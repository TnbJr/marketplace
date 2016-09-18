from django.conf import settings
from django.db import models
from django.dispatch import receiver 
from django.contrib.auth.models import User

from localflavor.us.us_states import US_STATES
# from orders.models import UserCheckout

# class Profile(models.Model):
# 	user = models.OneToOneField(User, related_name="profile")
# 	created = models.DateTimeField(auto_now_add=True)

# 	def __str__(self):
# 		return str(self.user)

	# @receiver(user_signed_up, sender=User)
	# def user_signed_up(request, user, *args, **kwargs):
	# 	if user:
	# 		profile = Profile.objects.get_or_create(user=user)

SHIPPING_CHOICE =(
	('10.00', 'Standard'),
	('20.00', 'Fast'),
	('90.00', 'Faster')
)


ADDRESS_TYPE = (
		('billing', 'Billing'),
		('shipping', 'Shipping'),
	)
NEW_STATE = US_STATES

class UserAddress(models.Model):
	user = models.ForeignKey(User)
	address = models.CharField(max_length=120)
	address2 = models.CharField(max_length=120, null=True, blank=True)
	city = models.CharField(max_length=120)
	state = models.CharField(max_length=120, choices=NEW_STATE, null=True, blank=True)
	country = models.CharField(max_length=120)
	zipcode = models.CharField(max_length=25)
	phone =  models.CharField(max_length=120)
	shipping = models.BooleanField(default=True)
	billing = models.BooleanField(default=False)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	def get_address(self):
		return "%s, %s, %s, %s" %(self.address, self.city, self.state, self.zipcode)

	def __str__(self):
		return str(self.user)