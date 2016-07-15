from django.conf.urls import url
from .views import CreateUser, LoginUser, UpdateUser, ChangePassword, logout
from django.contrib.auth.views import (
	password_reset,
	password_reset_done,
    password_reset_confirm
	)

urlpatterns = [
    # url(r'^$', index, name="index"),
    url(r'^create$', CreateUser.as_view(), name="signup"),
    url(r'^login$',  LoginUser.as_view(), name="login"),
    url(r'^update$', UpdateUser.as_view(), name="update"),
    url(r'^change-password$', ChangePassword.as_view(), name="password_change"),
    url(r'^reset-password$', password_reset, {'template_name': 'users/registration/password_reset_form.html', 'email_template_name':'users/registration/password_reset_email.html', 'post_reset_redirect': 'users:password_reset_done'}, name='password_reset'),
    url(r'^password-sent/$',password_reset_done,{'template_name':'users/registration/password_reset_done.html'}, name="password_reset_done"),
    url(r'^password-reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, {'post_reset_redirect' : '/user/password/done/', 'template_name':'users/registration/password_reset_email.html'}, name="password_reset_confirm"),
    
    # url(r'^welcome$', views.welcome, name="welcome"),
    url(r'^logout$', logout, name="logout"),
]