from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.base import View 
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.views.generic.detail import SingleObjectMixin, DetailView
from django.views.generic.edit import FormMixin

from orders.models import UserCheckout
from orders.forms import GuestCheckoutForm
from products.models import Variation
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

class CheckOutView(FormMixin, DetailView):
	model = Cart
	template_name = "carts/checkout.html"
	form_class = GuestCheckoutForm

	def get_object(self, *args, **kwargs):
		cart_id = self.request.session.get("cart_id")
		if cart_id == None:
			return redirect("cart:main")
		cart = Cart.objects.get(id=cart_id)
		return cart

	def get_context_data(self, *args, **kwargs):
		context = super(CheckOutView, self).get_context_data(*args, **kwargs)
		user_can_continue = False
		user_checkout_id = self.request.session.get("user_checkout_id")
		if not self.request.user.is_authenticated() or user_checkout_id == None:
			context["login_form"] = AuthenticationForm()
			context["next_url"] = self.request.build_absolute_uri()
		elif self.request.user.is_authenticated() or user_checkout_id != None:
			user_can_continue = True
		else:
			pass
		if self.request.user.is_authenticated():
			user_checkout, created = UserCheckout.objects.get_or_create(email=self.request.user.email)
			user_checkout.user = self.request.user
			user_checkout.save()
			self.request.session["user_checkout_id"] = user_checkout.id
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