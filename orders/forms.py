from django import forms
from django.contrib.auth import get_user_model


from users.models import UserAddress

User = get_user_model()

class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
			'user',
			'address',
			'address2',
			'city',
			'state',
			'country',
			'zipcode',
			'phone',
			'billing'
		]

class UserShippingForm(UserAddressForm):
	first_name = forms.CharField(label='First Name ')
	last_name = forms.CharField(label='Last Name ')
