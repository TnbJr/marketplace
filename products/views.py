import random 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.http import Http404
from django.contrib import messages 
from django.core.exceptions import ImproperlyConfigured
from django.views.generic import ListView, DetailView 
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from django_filters import FilterSet, CharFilter, NumberFilter

from .forms import ProductModelForm, VariationInventoryFormSet
from .mixins import StaffRequiredMixin, LoginRequiredMixin
from .models import Product, Variation, Category

from  django.views.generic.list import MultipleObjectMixin
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
		category_products = ( product_set | default_products).distinct()
		paginator = Paginator(category_products, 6) # Show 25 contacts per page
		page = self.request.GET.get('page')
		try:
			products = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			products = paginator.page(1)
		except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
			contacts = paginator.page(paginator.num_pages)
		context['products'] = products
		return context



class ProductDetailView(DetailView):
	model = Product
	template_name = "products/product_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
		instance = self.get_object()
		images = instance.productimage_set.all()
		images = images[1:5]
		context["related"] = sorted(Product.objects.get_related(instance)[:6], key = lambda x: random.random())
		context["images"] = images
		return context 



class ProductFilter(FilterSet):
	title = CharFilter(name='title', lookup_type ='icontains', distinct=True)
	category = CharFilter(name='categories__title', lookup_type ='icontains', distinct=True)
	category_id = CharFilter(name='categories__id', lookup_type ='icontains', distinct=True)
	min_price = NumberFilter(name='variation__price', lookup_type ='gte', distinct=True)
	max_price = NumberFilter(name='variation__price', lookup_type ='lte', distinct=True)
	class Meta:
		model = Product
		fields = [
			'title',
			'description',
		]

class FilterMixin(object):
	filter_class = None
	search_ordering_param = "ordering"

	def get_queryset(self, *args, **kwargs):
		try:
			qs = super(FilterMixin, self).get_queryset(*args, **kwargs)
			return qs
		except:
			raise ImproperlyConfigured("You must have a quersey to use the FilterMixin")

	def get_context_data(self, *args, **kwargs):
		context = super(FilterMixin, self).get_context_data(*args, **kwargs)
		qs = self.get_queryset()
		ordering = self.request.GET.get(self.search_ordering_param)
		if ordering: 
			qs = qs.order_by(ordering)
		filter_class = self.filter_class
		if filter_class:
			f = filter_class(self.request.GET, queryset=qs)
			context["object_list"] = f
		return context


class ProductListView(ListView, FilterMixin):
	model = Product
	queryset = Product.objects.all()
	paginate_by = 6
	template_name = "products/products-2.html"
	filter_class = ProductFilter

	def get_context_data(self, *args, **kwargs):
	    context = super(ProductListView, self).get_context_data(*args, **kwargs)
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
			try:
				qs2 = self.model.objects.filter(
					Q(price=query)
				)
				qs = (qs | qs2).distinct()
			except:
				pass
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
