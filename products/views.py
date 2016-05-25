import random 
from django.db.models import Q
from django.http import Http404
from django.contrib import messages 
from django.views.generic import ListView, DetailView 
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .forms import ProductModelForm, VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variation, Category

# Create your views here.

class CategoryListView(ListView):
	model = Category
	template_name = "products/list_view.html"


class CategoryDetailView(DetailView):
	model = Category
	template_name = "products/category_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(CategoryDetailView, self).get_context_data(*args, **kwargs)
		obj = self.get_object()
		product_set = obj.product_set.all()
		default_products = obj.default_category.all()
		products = ( product_set | default_products).distinct()
		context['products'] = Product.objects.get_related()
		return context



class ProductDetailView(DetailView):
	model = Product
	template_name = "products/detail_view.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key = lambda x: random.random())
		return context 


class ProductListView(ListView):
	model = Product
	queryset = Product.objects.all()
	template_name = "products/list_view.html"

	def get_context_data(self, *args, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(ProductListView, self).get_context_data(*args, **kwargs)
	    # Add in the publisher
	    context['now'] = timezone.now()
	    context['query'] = self.request.GET.get("q")
	    return context

	def get_queryset(self, *args, **kwargs):
		qs = super(ProductListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		if query:
			qs = self.model.objects.filter(
				Q(title__icontains=query) |
				Q(description__icontains=query)
				)
		return qs



class VariationListView(LoginRequiredMixin, ListView):
	model = Variation
	template_name = "products/variation_list.html"

	def get_context_data(self, *args, **kwargs):
	    # Call the base implementation first to get a context
	    context = super(VariationListView, self).get_context_data(**kwargs)
	    # Add in the publisher
	    context['formset'] = VariationInventoryFormSet(queryset=self.get_queryset())
	    return context

	def get_queryset(self, *args, **kwargs):
		qs = super(VariationListView, self).get_queryset(*args, **kwargs)
		query = self.request.GET.get("q")
		product_pk = self.kwargs.get("pk")
		if product_pk:
			product = get_object_or_404(Product, pk=product_pk)
			queryset = Variation.objects.filter(product=product)
		return queryset

	def post(self, request, *args, **kwargs):
		print(self.kwargs)
		formset = VariationInventoryFormSet(request.POST, request.FILES)
		if formset.is_valid():
			formset.save(commit=False)
			for form in formset:
				new_item = form.save(commit=False)
				product_pk = self.kwargs.get("pk")
				product = get_object_or_404(Product, pk=product_pk)
				new_item.product = product
				new_item.save()
				
				messages.success(request, "Your Inventory is valid")
			return redirect("product:variation_list", pk=product_pk)
		raise Http404
