from django.shortcuts import render, redirect 
from django.views.generic import View
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from itertools import chain
from operator import attrgetter


from products.models import Product

# Create your views here.
class IndexView(View):
	def get(self, request):
		feature_product = Product.objects.filter(featured=True)[:8]
		latest_product = Product.objects.filter(featured=False).order_by('-added_date')
		template = 'sitemaps/index.html'
		context = {
			"latest_products": latest_product,
			"feature_product": feature_product,
		}
		return render(request, template, context)
	
class AboutView(View):
	def get(self, request):
		return render(request, 'sitemaps/about.html')
		
class ShareView(View):
	def get(self, request):
		return render(request, 'sitemaps/share.html')




