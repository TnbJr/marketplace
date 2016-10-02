from django.conf.urls import url
from .views import UserAddressCreateView, OrderList, OrderDetail

urlpatterns = [
    url(r'^address/create$',  UserAddressCreateView.as_view(), name='address_create'),
    url(r'^(?P<pk>\d+)$', OrderDetail.as_view(), name='order_detail'),
    url(r'^$',  OrderList.as_view(), name='orders_list'),
]