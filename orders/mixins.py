from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from carts.models import Cart
from .models import Order

class LoginRequiredMixin(object):
	
	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

class CartOrderMixin(object):
	def get_order(self, *args, **kwargs):
		cart = self.get_cart()
		if cart is None:
			print("THe cart is none")
			return None
		new_order_id = self.request.session.get("order_id")
		if new_order_id is None:
			print('new order is None')
			new_order = Order.objects.create(cart=cart)
			self.request.session["order_id"] = new_order.id
		else:
			print("new_order is valid")
			new_order = Order.objects.get(id=new_order_id)
			# print(new_order)
		return new_order

	def get_cart(self, *args, **kwargs):
		cart = self.request.session.get("cart_id")
		if cart == None:
			return None
		cart = Cart.objects.get(id=cart)
		if cart.items.count() <= 0:
			return None
		return cart