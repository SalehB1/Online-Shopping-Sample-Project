from django.urls import path
from .views import SupplierLogin, SellerLogout, SellerRegister

urlpatterns = [
    path('', SupplierLogin.as_view(), name='sellerLogin'),
    path('seller_logout/', SellerLogout.as_view(), name='sellerLogout'),
    path('seller_register/', SellerRegister.as_view(), name='sellerRegister'),

]
