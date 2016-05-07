from django.views.generic import ListView, DetailView 
from django.shortcuts import render
from django.utils import timezone
from .forms import ProductModelForm
from .models import Product

# Create your views here.

class ProductDetailView(DetailView):
	model = Product
	template_name = "products/detail_view.html"

class ProductListView(ListView):
	model = Product
	template_name = "products/list_view.html"

	def get_context_data(self, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(ProductListView, self).get_context_data(**kwargs)
	    # Add in the publisher
	    context['now'] = timezone.now()
	    return context