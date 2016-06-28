"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^article/', include('posts.urls', namespace='post')),
    url(r'^profile/', include('users.urls', namespace='profile')),
    url(r'^product/', include('products.urls', namespace='product')),
    url(r'^category/', include('products.urls_categories', namespace='category')),
    url(r'^cart/', include('carts.urls', namespace='cart')),
    url(r'^contact/', include('contacts.urls', namespace='contact')),
    url(r'^order/', include('orders.urls', namespace='order')),
    url(r'^newsletter/', include('newsletters.urls', namespace='newsletter')),
    url(r'^', include('sitemaps.urls', namespace='sitemap')),
]


if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)