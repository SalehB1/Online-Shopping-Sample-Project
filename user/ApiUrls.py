from django.urls import path
from .apiView import ClientRegisterView, GetTokenForLoginView, ClientProfileView
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('client/register/', ClientRegisterView.as_view(), name='clientRegister'),
    path('client/login/', GetTokenForLoginView.as_view(), name='clientLogin'),
    path('client/login/refresh/', TokenRefreshView.as_view(), name='clientLogin_refresh'),
    path('client/profile/', ClientProfileView.as_view(), name='clientProfile'),
]