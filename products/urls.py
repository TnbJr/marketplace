from django.conf.urls import url
from products.views import ProductListView, ProductDetailView, VariationListView

urlpatterns = [
    url(r'^detail/(?P<pk>[\d]+)$', ProductDetailView.as_view(), name='detail'),
    url(r'^detail/(?P<pk>[\d]+)/inventory$', VariationListView.as_view(), name='variation_list'),
    # url(r'^create$', 'products.views.create_view', name='create'),
    # url(r'^$', 'products.views.product_list', name='list'),
    url(r'^$',  ProductListView.as_view(), name='list')
]
