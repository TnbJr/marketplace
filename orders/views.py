from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse
# Create your views here.
from .mixins import CartOrderMixin, LoginRequiredMixin
from .forms import UserAddressForm
from .models import UserAddress, UserCheckout, Order


class OrderDetail(LoginRequiredMixin, DetailView):
	model = Order

	def dispatch(self, request, *args, **kwargs):
		try:
			user_checkout_id = self.request.session.get("user_checkout_id")
			user_checkout =  UserCheckout.objects.get(id=user_checkout_id)
			("session info valid", user_checkout)
		except UserCheckout.DoesNotExist:
			user_checkout = UserCheckout.objects.get(user=request.user)
			print("user does not exist exception ", user_checkout)
		except:
			user_checkout = None
			("your shit not valid user checkout")
		obj = self.get_object()
		if obj.user == user_checkout.user and user_checkout is not None:
			print("dispatch is working")
			return super(OrderDetail, self).dispatch(request, *args, **kwargs)
		else:
			print("this is the object usear", obj.user)
			print ("this the userchekout before 404", user_checkout)
			print(obj.user == user_checkout.user)
			print("obj user type ", type(obj.user))
			print("user_checl=kout type ", type(user_checkout))
			raise Http404

class OrderList(LoginRequiredMixin, ListView):
	queryset = Order.objects.all()

	def get_queryset(self):
		user_checkout_id = self.request.session.get("user_checkout_id")
		print(user_checkout_id)
		print(self.request.user.id)
		user_checkout = UserCheckout.objects.get(id=user_checkout_id)
		return super(OrderList, self).get_queryset().filter(user=user_checkout)


class UserAddressCreateView(CreateView):
	form_class = UserAddressForm
	template_name = "orders/address.html"
	success_url = "/order/address"

	def get_checkout_user(self):
		user_checkout_id = self.request.session.get("user_checkout_id")
		user_checkout =  UserCheckout.objects.get(id=user_checkout_id)
		return user_checkout

	def form_valid(self, form, *args, **kwargs):
		form.instance.user = self.get_checkout_user()
		return super(UserAddressCreateView, self).form_valid(form, *args, **kwargs)


