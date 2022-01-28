from django.urls import path
from .apiView import ClientRegisterView, GetTokenForLoginView, ClientProfileView, ClientOtpGenerator, ActivateUserPhone, \
    LoginWithOtp
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('client/register/', ClientRegisterView.as_view(), name='clientRegister'),
    path('client/login/', GetTokenForLoginView.as_view(), name='clientLogin'),
    path('client/login/refresh/', TokenRefreshView.as_view(), name='clientLogin_refresh'),
    path('client/profile/', ClientProfileView.as_view(), name='clientProfile'),
    path('api/generateotp/', ClientOtpGenerator.as_view(), name='generateotp'),
    path('api/activeuserphone/', ActivateUserPhone.as_view(), name='activepohne'),
    path('api/loginwithotp/', LoginWithOtp.as_view(), name='loginwithotp')
]
