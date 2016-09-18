from django import forms
from django.contrib.auth import get_user_model


from .models import UserAddress

User = get_user_model()


# class UserShippingForm(forms.ModelForm):
# 	first_name = forms.CharField(label='First Name ')
# 	last_name = forms.CharField(label='Last Name ')
# 	class Meta:
# 		model = UserShippingInfo
# 		fields = [
# 			'user',
# 			'shipping_choice',
# 			'street',
# 			 'city',
# 			 'state',
# 			 'zipcode',
# 			 'phone_number'
# 		]
# 		widgets = {
# 			'shipping_choice': forms.RadioSelect(),
# 		}
		# labels = {
  #           'shipping_choice': 'Writer',
  #       }

# class AddressForm(forms.Form):
# 	billing_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(
# 		address_type="billing"),
# 		empty_label= None,
# 		widget= forms.RadioSelect,

# 	)
# 	shipping_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(
# 		address_type="shipping"),
# 		empty_label= None,
# 		widget= forms.RadioSelect,

# 	)

class UserAddressForm(forms.ModelForm):
	class Meta:
		model = UserAddress
		fields = [
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
