from django.views.generic import View, ListView, DetailView, UpdateView, DeleteView, CreateView
from django.core.urlresolvers import reverse_lazy
from django.http import Http404
from django.contrib.auth.decorators import login_required 
from django.shortcuts import render,redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from urllib.parse import quote_plus
from django.utils import timezone
# from braces.views import StaffuserRequiredMixin
from .forms import ContentPostForm
from .models import ContentPost

class StaffuserRequiredMixin(object):
	pass
# Create your views here.
class CategoryIndexView(StaffuserRequiredMixin, View):
	template = "posts/index.html"
	def get(self, request):
		queryset = ContentPost.objects.all()
		context={
			"queryset": queryset
		}
		return render(request, self.template, context)

class CategoryDetailView(View):
	template = "posts/category_detail.html"
	def get(self, request, slug):
		queryset_list = ContentPost.objects.filter(categories=slug, draft=False, published__lte=timezone.now())
		if not queryset_list:
			raise Http404
		
		paginator = Paginator(queryset_list, 2) # Show 10 contacts per page

		page = request.GET.get('page')
		try:
			queryset = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			queryset = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver last page of results.
			queryset = paginator.page(paginator.num_pages)
		context = {
			"title": slug,
			"queryset": queryset,
		}
		return render(request, self.template, context)


class PostCreateView(StaffuserRequiredMixin, CreateView):
	model = ContentPost
	template_name = "posts/post_create.html"
	fields = ['title','image', 'content', 'draft','published','categories','source']
	# form = ContentPostForm

	def get_context_data(self, *args, **kwargs):
		context = super(PostCreateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Create New Content"
		return context



class PostDeleteView(StaffuserRequiredMixin, DeleteView):
	model = ContentPost
	template_name = "posts/post_delete.html"
	success_url = reverse_lazy('post:index-post')

	def get_context_data(self, *args, **kwargs):
		context = super(PostDeleteView, self).get_context_data(*args, **kwargs)
		context['title'] = "Delete Content"
		return context
 

class PostDetailView(DetailView):
	model = ContentPost
	template_name = "posts/post_detail.html"

	def get_context_data(self, *args, **kwargs):
		context = super(PostDetailView, self).get_context_data(*args, **kwargs)
		_object = self.get_object()
		share_string = quote_plus(_object.title)
		context['share_string'] = share_string
		return context


class PostIndexView(ListView):
	model = ContentPost
	paginate_by = 3
	template_name = "posts/index.html"

	def get_context_data(self, *args, **kwargs):
		context = super(PostIndexView, self).get_context_data(*args, **kwargs)
		context['posts'] = ContentPost.objects.filter(draft=False, published__lte=timezone.now())
		return context


class PostUpdateView(StaffuserRequiredMixin, UpdateView):
	model = ContentPost
	template_name = "posts/post_update.html"
	form_class = ContentPostForm
	
	def get_context_data(self, *args, **kwargs):
		context = super(PostUpdateView, self).get_context_data(*args, **kwargs)
		context['title'] = "Update Content"
		return context
     
