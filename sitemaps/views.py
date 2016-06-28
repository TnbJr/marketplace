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
		feature_product = Product.objects.filter(featured=False)[:8]
		latest_product = Product.objects.filter(featured=True).order_by('-added_date')
		# page_template = 'post.html'
		template = 'sitemaps/index.html'
		context = {
			"latest_products": latest_product,
			"feature_product": feature_product,
			# "signup_form": form,
			# "query": queryset,
			# "main_featured": featured_item.first(), 
			# "other_featured": featured_item[1:5],
		}
		return render(request, template, context)


	
class AboutView(View):
	def get(self, request):
		return render(request, 'sitemaps/about.html')
		
class ShareView(View):
	def get(self, request):
		return render(request, 'sitemaps/share.html')

# class ContactView(View):
# 	title = "Contact Us"
# 	form = ContactForm
# 	template = "contacts/contact.html"
# 	def get(self, request):
# 		context ={
# 			"title": self.title,
# 			"form": self.form(request.POST or None),
# 		}
# 		return render(request, self.template, context)

# 	def post(self, request):
# 		form = self.form(request.POST or None)
# 		if form.is_valid():
# 			name = form.cleaned_data['name']
# 			subject = form.cleaned_data['subject']
# 			message = form.cleaned_data['message']
# 			emailFrom = form.cleaned_data['email']
# 			emailTo = [settings.EMAIL_HOST_USER]
# 			send_mail(subject, message, emailFrom, emailTo, fail_silently=False)
# 			form.save()
# 			messages.success(request, 'We have received your message')
# 			return redirect('contact:contact')
# 		context ={
# 		"title": self.title,
# 		"form": self.form(request.POST or None),
# 		}
# 		return render(request, self.template, context)



