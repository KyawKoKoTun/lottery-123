from rest_framework import serializers
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.hashers import make_password, check_password


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        email = data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "User does not exist")
        if check_password(data['password'], user.password):
            data['user'] = user
            return data
        else:
            raise serializers.ValidationError(
                "Invalid email or password.")


class UserRegistrationSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class DiscountPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscountPeriod
        fields = '__all__'


class OrderKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderKey
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    order_key = OrderKeySerializer()

    class Meta:
        model = Order
        fields = '__all__'


class WinningTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningType
        fields = '__all__'


class ProfileEditSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    profile_picture = serializers.ImageField(required=False)


class LotteryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LotteryType
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class WinningTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WinningType
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'


class TermsAndConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermAndCondition
        fields = '__all__'


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaLink
        fields = '__all__'
