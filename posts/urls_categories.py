from django.conf.urls import url
from .views import CategoryIndexView, CategoryDetailView

urlpatterns = [
	url(r'^category$',  CategoryIndexView.as_view(), name='index-category'),
	url(r'^(?P<slug>[\w-]+)$',  CategoryDetailView.as_view(), name='detail-category'),
]