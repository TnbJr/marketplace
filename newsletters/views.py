from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .models import SignUp


class NewsLetterView(View):
	template = "newsletters/newsletter.html"
	form = SignUpForm
	def get(self, request):
		context = {
			"signup_form": self.form()
		}
		return render(request, self.template, context)

	def post(self, request):
		form = self.form(request.POST or None)
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			return redirect('sitemaps:share')
		context = {
		"signup_form": self.form(request.POST or None), 
		}
		return render(request, self.template, context)
