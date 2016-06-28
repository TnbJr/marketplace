from django.conf.urls import url
from .views import NewsLetterView

urlpatterns = [
	url(r'^$',  NewsLetterView.as_view(), name='newsletter'),
]