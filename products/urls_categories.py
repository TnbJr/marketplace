from django.conf.urls import url
from products.views import CategoryListView, CategoryDetailView


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)$', CategoryDetailView.as_view(), name='detail'),
    url(r'^$', CategoryListView.as_view(), name='list')
]
