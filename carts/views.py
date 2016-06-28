import braintree

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View 
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

from orders.models import UserCheckout, Order, UserAddress
from orders.forms import GuestCheckoutForm, UsertAddressForm
from orders.mixins import CartOrderMixin
from products.models import Variation
from .models import Cart, CartItem

from allauth.account.forms import LoginForm

# Create your views here.

class ItemCountView(View):
	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			cart_id = self.request.session.get("cart_id")
			if cart_id == None:
				count = 0
			else:
				cart = Cart.objects.get(id=cart_id)
				count = cart.items.count()
			request.session["cart_item_count"] = count
			return JsonResponse({"count": count})
		else:
			raise Http404

class CartView(SingleObjectMixin, View):
	model = Cart
	template_name = "carts/carts.html"

	def get_object(self, *args, **kwargs):
		# request.session.set_expiry()
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(id=cart_id)
		if self.request.user.is_authenticated():
			cart.user = self.request.user
			cart.save()
		return cart


	def get(self, request):
		cart = self.get_object()
		item_id = request.GET.get("item")
		delete_item = request.GET.get("delete", False)
		item_added = False
		flash_message = ""
		if item_id:
			item_instance = get_object_or_404(Variation, id=item_id)
			qty = request.GET.get("qty", 1)
			try:
				if int(qty) < 1:
					delete_item = True
			except:
				raise Http404
			cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item_instance)
			if created:
				flash_message = "Successfully Added To Cart"
				item_added = True
			if delete_item:
				flash_message = "Item Removed"
				cart_item.delete()
			else:
				flash_message = "Quantity Updated"
				cart_item.quantity = qty
				cart_item.save()
			if not request.is_ajax():
				return HttpResponseRedirect(reverse("cart:main"))
				
		if request.is_ajax():
			try:
				total = cart_item.item_total
			except:
				total = None
			try:
				subtotal = cart_item.cart.subtotal
			except:
				subtotal = None
			try:
				cart_total = cart_item.cart.total
			except:
				cart_total = None
			try:
				tax_total = cart_item.cart.tax_total
			except:
				tax_total = None
			try:
				total_items = cart_item.cart.items.count()
			except:
				total_items = 0

			data = {
					"deleted": delete_item,
					"item_added": item_added,
					"line_total": total,
					"cart_total": cart_total,
					"tax_total": tax_total,
					"subtotal": subtotal,
					"flash_message": flash_message,
					"total_items": total_items
					}
			return JsonResponse(data)
		context = {
			"object": self.get_object
		}
		return render(request, self.template_name, context)
	

class CheckOutView(CartOrderMixin, FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout.html"
	form_class = UsertAddressForm

	def get_object(self, *args, **kwargs):
		cart = self.get_cart()
		if cart == None:
			return None
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super(CheckOutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_checkout_id = self.request.session.get("user_checkout_id")
		if self.request.user.is_authenticated():
			user_can_continue = True
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()
			self.request.session["user_checkout_id"] = user_checkout.id
		elif not self.request.user.is_authenticated() and user_checkout_id == None:
			context["login_form"] = LoginForm
			context["next_url"] = self.request.build_absolute_uri()
		else:
			pass
		if user_checkout_id != None:
			user_can_continue = True
			if not self.request.user.is_authenticated():
				user_checkout_2 = UserCheckout.objects.get(id=user_checkout_id)
				context["client_token"] = user_checkout_2.get_client_token()
		context["order"] = self.get_order()
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			# print("jakk")
			# print(form.cleaned_data.get("verify_email"))
			user_checkout, created = UserCheckout.objects.get_or_create(email=email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
		else:
			# print(form.cleaned_data.get("email"))
			return self.form_invalid(form)

	def get_success_url(self):
		return reverse("cart:checkout")

	def get(self, request, *args, **kwargs):
		print("checkout get call")
		cart = self.get_object()
		new_order = self.get_order()
		user_checkout_id = request.session.get("user_checkout_id")
		print(user_checkout_id)
		if user_checkout_id != None:
			user_checkout = UserCheckout.objects.get(id=user_checkout_id)
			if new_order.billing_address == None or new_order.shipping_address == None:
				print("needs address")
				return redirect("order:address_select")
			new_order.user = user_checkout
			new_order.save()
		return super(CheckOutView, self).get(request, *args, **kwargs)

class FinanlizeCheckoutView(CartOrderMixin, View):
	def post(self, request, *args, **kwargs):
		order = self.get_order()
		nonce = request.POST.get("payment_method_nonce")
		if nonce:
			result = braintree.Transaction.sale({
			    "amount": order.order_total,
			    "payment_method_nonce": nonce,
			    "billing": {
			    	"postal_code": "%s" %(order.billing_address.zipcode),
			    },
			    "options": {
			        "submit_for_settlement": True
			    }    
			})
		if result.is_success:
			order.mark_completed(order_id=result.transaction.id)
			messages.success(request, "Thank you for your order")
			del request.session["cart_id"]
			del request.session["order_id"]
		else:
			messages.success(request,"%s" %(result.message))
		return redirect("order:order_detail", pk=order.pk )

	def get(self, request, *args, **kwargs):
		return redirect("cart:checkout")
