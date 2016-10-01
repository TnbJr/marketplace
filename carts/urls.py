from django.conf.urls import url
from .views import CartView, ItemCountView, CheckOutView, FinanlizeCheckoutView, CheckOutApiView

urlpatterns = [
    # url(r'^detail/(?P<pk>[\d]+)$', ProductDetailView.as_view(), name='detail'),
    # url(r'^detail/(?P<pk>[\d]+)/inventory$', VariationListView.as_view(), name='variation_list'),
    # url(r'^create$', 'products.views.create_view', name='create'),
    
    url(r'^count$',  ItemCountView.as_view(), name='count'),
    url(r'^checkout$',  CheckOutView.as_view(), name='checkout'),
    url(r'^checkout/final$',  FinanlizeCheckoutView.as_view(), name='final'),
    url(r'^api/checkout$',  CheckOutApiView.as_view(), name='api_checkout'),
    url(r'^$',  CartView.as_view(), name='main')
]