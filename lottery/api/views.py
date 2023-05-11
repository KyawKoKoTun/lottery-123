from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from .models import *
from rest_framework import permissions
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
import hashlib
import secrets

import threading
import time
import random


def task():

    for lottery in LotteryType.objects.all():
        current_number = ''
        counter = 1
        for digit in range(lottery.number_of_digits):
            current_number += str(random(0, 9)) + \
                '_' if counter != lottery.number_of_digits else str(
                    random(0, 9))
            counter += 1
        lottery.current_number = current_number
        lottery.save()

    for order in Order.objects.all():
        user = order.user
        if order.bet_digits == order.lottery_type.current_number:
            prize = WinningType.objects.get(
                lottery_type=order.lottery_type, name='straight').prize
            user.balance += prize
            user.save()
            order.winning_type = 'Straight'
            order.won_prize_amount = prize
            order.save()
            Notification.objects.create(
                user=user, text='Congratulation! You have won a prize!').save()
        else:
            bet_digits = order.bet_digits.split(' ').sort()
            draw_digits = order.lottery_type.current_number.split(' ').sort()
            if bet_digits == draw_digits:
                prize = WinningType.objects.get(
                    lottery_type=order.lottery_type, name='rumble').prize
                user.balance += prize
                user.save()
                order.winning_type = 'Straight'
                order.won_prize_amount = prize
                order.save()
                Notification.objects.create(
                    user=user, text='Congratulation! You have won a rumble prize!').save()
            else:
                order.winning_type = 'Lost'
                order.save()

    time.sleep(3600*24)
    threading.Thread(target=task).start()


task_started = False


class StartTaskView(APIView):
    @csrf_exempt
    def get(self, request):
        user = token_to_user(request)
        if user.is_staff:
            global task_started
            if not task_started:
                threading.Thread(target=task).start()
                task_started = True
                return Response({'detail': 'started.'})
            else:
                return Response({'detail': 'already started.'})
        else:
            return Response({'detail': 'You are not a staff user.'}, status=401)


def token_to_user(request):
    auth_header = request.headers.get('Authorization')
    if not auth_header:
        raise AuthenticationFailed('Authentication header missing')
    auth_token = auth_header.split(' ')[1]

    token_auth = TokenAuthentication()
    try:
        user, _ = token_auth.authenticate_credentials(auth_token)
        user = User.objects.filter(username=user.username).first()
        return user
    except AuthenticationFailed:
        raise AuthenticationFailed('Invalid token')


class UserLoginView(APIView):
    serializer_class = UserLoginSerializer

    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserRegistrationView(APIView):
    serializer_class = UserRegistrationSerializer

    @csrf_exempt
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class UserView(APIView):
    serializer_class = UserSerializer

    @csrf_exempt
    def get(self, request):
        user = token_to_user(request)
        serializer = self.serializer_class(user)
        return Response(serializer.data)


class ProfileEditView(APIView):
    serializer_class = ProfileEditSerializer

    @csrf_exempt
    def post(self, request):
        user = token_to_user(request)
        serializer = self.serializer_class(
            user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Profile updated successfully'})


class OrderView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class OrderKeyGetView(APIView):

    def get(self, request):
        random_string = secrets.token_hex(16)
        sha256_hash = hashlib.sha256(random_string.encode()).hexdigest()
        user = token_to_user(request)
        order_key = OrderKey.objects.create(user=user, key=sha256_hash)
        order_key.save()
        return Response({'key': sha256_hash})


class OrderSubmitView(APIView):
    def post(self, request):
        user = token_to_user(request)
        lottery_type_id = request.data.get('lottery_type_id')
        lottery_type = get_object_or_404(LotteryType, id=lottery_type_id)

        order_key = get_object_or_404(OrderKey, key=request.data['key'])

        order = Order.objects.create(
            user=user, lottery_type=lottery_type, order_key=order_key, bet_digits=request.data['bet_digits'])
        order.save()

        if user.balance < lottery_type.draw_price:
            return Response({'message': 'You do not have enough balance to submit this order!'},
                            status=status.HTTP_400_BAD_REQUEST)

        user.balance -= lottery_type.draw_price
        user.save()

        return Response({'message': 'Order submitted successfully!', 'order_id': order.id},
                        status=status.HTTP_200_OK)


class OrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = token_to_user(self.request)
        return Order.objects.filter(user=user)


class DiscountPeriodView(generics.RetrieveAPIView):
    serializer_class = DiscountPeriodSerializer

    def get_queryset(self):
        return get_object_or_404(DiscountPeriod, user=token_to_user(self.request))


class BuyDiscountView(APIView):
    def post(self, request):
        user = token_to_user(request)
        try:
            discount_period = user.discount_periods.first()
            if discount_period.end_date < datetime.now():
                discount_period.end_date = datetime.now() + \
                    timedelta(days=365)
            else:
                discount_period.end_date = discount_period.end_date + \
                    timedelta(days=365)
            discount_period.save()
        except DiscountPeriod.DoesNotExist:
            end_date = datetime.now() + timedelta(days=365)
            discount_period = DiscountPeriod.objects.create(
                user=user, end_date=end_date, discount_percentage=20)

        return Response({'message': 'Discount bought successfully!'}, status=status.HTTP_200_OK)


class LotteryTypesView(generics.ListAPIView):
    serializer_class = LotteryTypeSerializer
    queryset = LotteryType.objects.all()


class NotificationsView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        user = token_to_user(self.request)
        return user.notifications.all()


class WinningTypesView(generics.ListAPIView):
    serializer_class = WinningTypeSerializer
    queryset = WinningType.objects.all()


class AboutUsView(generics.RetrieveAPIView):
    serializer_class = AboutUsSerializer
    queryset = AboutUs.objects.first()


class ContactsView(generics.ListAPIView):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class TermsAndConditionsView(generics.RetrieveAPIView):
    serializer_class = TermsAndConditionsSerializer
    queryset = TermAndCondition.objects.first()


class PrivacyPolicyView(generics.RetrieveAPIView):
    serializer_class = PrivacyPolicySerializer
    queryset = PrivacyPolicy.objects.first()


class SocialsView(generics.RetrieveAPIView):
    serializer_class = SocialSerializer
    queryset = SocialMediaLink.objects.all()
