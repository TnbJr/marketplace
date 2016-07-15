from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView
from django.views.generic.detail import DetailView

from .models import Profile
from .forms import ProfileForm, UserUpdateForm, UserCreateForm
# from reviews.models import UserReview
from django.utils.decorators import method_decorator

from django.views.decorators.http import require_http_methods

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import (
		UserCreationForm, AuthenticationForm, PasswordChangeForm
	)

from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
# Create your views hee.

@require_http_methods(['GET'])
def index(request):
	if request.method == "GET":
		if "next" in request.GET:
			request.session["next"] = request.GET["next"]
		return render(request, "users/index.html")

@method_decorator([login_required, require_http_methods(['GET'])])
def welcome(request):
	if request.method == "GET":
		logout(request)
		return redirect(settings.LOGIN_URL)

class CreateUser(View):
	template_name = "user_form.html"
	form_class = UserCreateForm
	success_url = "users:login"

	def get(self, request):
		form = self.form_class()
		context = self.get_context(form)
		return render(request, self.template_name, context)

	def post(self, request):
		form = self.form_class(data=request.POST)
		if form.is_valid():
			user = form.save()
			# help_.finalize_user(user)
			return redirect(self.success_url)
		else:
			context = self.get_context(form)
			return render(request, self.template_name, context)

	def get_context(self, form):
		return{
			"form": form,
			"action": "users:signup",
			"method": "POST",
			"submit_text": "Register"
		}

class LoginUser(FormView):
	template_name = "user_form.html"
	form_class = AuthenticationForm
	success_url = "/"

	# def get(self, request):
	#   form = self.form_class()
	#   context = self.get_context_data(form)
	#   return render(request, self.template_name, context)
	@method_decorator(csrf_protect)
	def post(self, request, *args, **kwargs):
		form_class = self.get_form_class()
		form = self.get_form(form_class)
		if form.is_valid():
			print('The post login post is valid')
			return self.form_valid(form)
			# form = self.form_class(request)
			# print(form)
			# print(form.get_user())
			# print('Users login get called')
			# if form.is_valid():
			#     user = form.get_user()
			#     print(user)

			#     login(request, user)
			#     # if "next" in request.session:
			#     #   self.success_url = request.session["next"]
			#     #   del request.session["next"]
			#     request.session.set_exipry(300)
			#     return redirect(self.success_url)
		else:
			print('whst the fuck man')
			print(form.errors)
			return self.form_invalid(form)
			# context = self.get_context(form)
			# return render(request, self.template_name, context)

	def get_context_data(self, *args, **kwargs):
	  context = super(LoginUser, self).get_context_data(*args, **kwargs)
	  # context["form"] = form
	  context["action"] = "users:login"
	  context["method"] = "POST"
	  context["submit_text"] = "Login"
	  return context

	def form_valid(self, form):
		print('Form valid')
		print(self.request.session._session_key)
		# print(self.request.POST['name'])
		# print(self.request.POST['title'])
		auth_login(self.request, form.get_user())
		# billing_address = form.cleaned_data["billing_address"]
		# shipping_address = form.cleaned_data["shipping_address"]
		# order = self.get_order()
		# order.billing_address = billing_address
		# order.shipping_address = shipping_address
		# order.save()
		# self.request.session["billing_address"] = billing_address.id
		# self.request.session["shipping_address"] = shipping_address.id

		return super(LoginUser, self).form_valid(form)
		
	def form_invalid(self, form):
		print('invalid login form')
		"""
		If the form is invalid, re-render the context data with the
		data-filled form and errors.
		"""
		return self.render_to_response(self.get_context_data(form=form))

	def get_success_url(self):
		# next_url = self.request.POST.get('next',None) # here method should be GET or POST.
		
		next_url = self.request.GET.get('next')
		print(next_url)
		if next_url:
			print('next works')
			return next_url
		print('next not working')
		return self.success_url
			# you can include some query strings as well
		# redirect_to = self.request.REQUEST.get(self.redirect_field_name)
		# if not is_safe_url(url=redirect_to, host=self.request.get_host()):
		#   redirect_to = self.success_url
		# return redirect_to


class UpdateUser(LoginRequiredMixin, View):
	template_name = "user_form.html"
	form_class = UserUpdateForm
	success_url = "users:welcome"

	def get(self, request):
		print("get")
		form = self.form_class(instance=request.user)
		context = self.get_context(form)
		return render(request, self.template_name, context)

	def post(self, request):
		print("POST")
		form = self.form_class(
			data=request.POST, instance=request.user
			)
		if form.is_valid():
			print("valid")
			form.save()
			return redirect(self.success_url)
		else:
			print(data)
			print('slime')
			context = self.get_context(form)
			return render(request, self.template_name, context)

	def get_context(self, form):
		return {
			"form": form,
			"action": "users:update",
			"method": "POST",
			"submit_text": "Update"
		}

class ChangePassword(LoginRequiredMixin, View):
	template_name = "users/redgistration/password_change_form.html"
	form_class = PasswordChangeForm
	success_url = "user:welcome"

	def get(self, request):
		form = self.form_class(user=request.user)
		context = self.get_context(form)
		return render(request, self.template_name, context)

	def post(self, request):
		form = self.form_class(
				data=request.POST, instance=request.user
			)
		if form.is_valid():
			form.save()
			return redirect(self.success_url)
		else:
			context = self.get_context(form)
			return render(request, self.template_name, context)

	def get_context(self, form):
		return {
			"form": form,
			"action": "users:password_change",
			"method": "POST",
			"submit_text": "Update"
		}

def logout(request): pass 




