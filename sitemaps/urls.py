from django.conf.urls import include, url
from .views import IndexView, AboutView, ShareView
# from newsletters.views import NewsLetterView

urlpatterns = [
	url(r'^$',  IndexView.as_view(), name='index'),
	url(r'^about$',  AboutView.as_view(), name='about'),
	# url(r'^share$', NewsLetterView.as_view(), name='share'),
]