from django.urls import path
from .views import CustomerList, OrderChart, OrderEditstatus, OrderList, ProductList, OrderDetail


urlpatterns = [
    path('order_list/<slug:slug>/', OrderList.as_view(), name='order_list'),
    path('product_list/<slug:slug>/', ProductList.as_view(), name='product_list'),
    path('order_detail/<slug:slug>/<int:id>/', OrderDetail.as_view(), name='order_detail'),
    path('order_eidt_status/<slug:slug>/<int:pk>/', OrderEditstatus.as_view(), name='order_status'),
    path('customer_list/<slug:slug>/', CustomerList.as_view(), name='customer_list'),
    path('chart/<slug:slug>/', OrderChart.as_view(), name='order_chart'),

]