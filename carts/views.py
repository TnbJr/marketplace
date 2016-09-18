import braintree

from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View 
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin
from orders.models import UserCheckout
from orders.forms import UserAddressForm, UserShippingForm
from orders.mixins import CartOrderMixin, LoginRequiredMixin
from products.models import Variation
from users.models import UserAddress
from .models import Cart, CartItem


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
			print('cart_id is none')
			cart = Cart()
			cart.save()
			cart_id = cart.id
			self.request.session["cart_id"] = cart_id
		cart = Cart.objects.get(pk=cart_id)
		if self.request.user.is_authenticated():
			cart.user = self.request.user

			cart.save()
		return cart

	def get(self, request):
		print('han')
		print(self.request.user)
		print(self.request.session.get("cart_id"))
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
			"object": self.get_object(),
			"user_address": UserAddress.objects.filter(user=self.request.user)
		}
		return render(request, self.template_name, context)
	

class CheckOutView(LoginRequiredMixin, CartOrderMixin, FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout.html"
	form_class = UserShippingForm

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
			# user_profile = Profile.objects.get(user=self.request.user)
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user

			user_checkout.save()
			context["client_token"] = user_checkout.get_client_token()
			self.request.session["user_checkout_id"] = user_checkout.id
		if user_checkout_id != None:
			user_can_continue = True
			if not self.request.user.is_authenticated():
				user_checkout_2 = UserCheckout.objects.get(id=user_checkout_id)
				context["client_token"] = user_checkout_2.get_client_token()
		context["order"] = self.get_order()
		context["user_can_continue"] = user_can_continue
		context["form"] = self.get_form()
		context["user_address"] = UserAddress.objects.filter(user=self.request.user)
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = self.get_form()
		if form.is_valid():
			email = form.cleaned_data.get("email")
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			request.session["user_checkout_id"] = user_checkout.id
			return self.form_valid(form)
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
			new_order.user = self.request.user
			new_order.save()
		return super(CheckOutView, self).get(request, *args, **kwargs)

	def get_initial(self):
		initial = super(CheckOutView, self).get_initial()
		initial['first_name'] = self.request.user.first_name
		initial['last_name'] = self.request.user.last_name
		return initial

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
