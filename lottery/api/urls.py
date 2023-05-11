from django.urls import path
from .views import *

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/', UserView.as_view(), name='user'),
    path('profile-edit/', ProfileEditView.as_view(), name='profile edit view'),

    path('start-task/', StartTaskView.as_view(), name='start task'),

    path('notifications/', NotificationsView.as_view(), name='notifications view'),

    path('orders/<int:pk>', OrderView.as_view(), name='single order view'),
    path('order/<int:id>/', OrdersView.as_view(), name='orders list view'),
    path('order/get-key/', OrderKeyGetView.as_view(), name='get order key'),
    path('order/submit/', OrderSubmitView.as_view(), name='order submit'),

    path('lottery-types/', LotteryTypesView.as_view(), name='lottery types view'),
    path('winning-types/<int:id>', WinningTypesView.as_view(), name='winning types'),

    path('discount/current/', DiscountPeriodView.as_view(), name='discount period'),
    path('discount/buy/', BuyDiscountView.as_view(), name='buy discount coupon'),

    path('about-us/', AboutUsView.as_view(), name='about us view'),
    path('contacts/', ContactsView.as_view(), name='contacts view'),
    path('terms/', TermsAndConditionsView.as_view(),
         name='terms and conditions view'),
    path('privacy-policy/', PrivacyPolicyView.as_view(),
         name='privacy policy view'),
    path('socials/', SocialsView.as_view(), name='socials view'),
]
