from django.conf.urls import url
from products.views import ProductListView, ProductDetailView

urlpatterns = [
    url(r'^detail/(?P<pk>[\d]+)$', ProductDetailView.as_view(), name='detail'),
    # url(r'^create$', 'products.views.create_view', name='create'),
    url(r'^$',  ProductListView.as_view(), name='list')
]
