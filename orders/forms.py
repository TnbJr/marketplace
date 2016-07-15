from django import forms
from django.contrib.auth import get_user_model
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout


from .models import UserAddress

User = get_user_model()

class GuestCheckoutForm(forms.Form):
	email = forms.EmailField()
	email2 = forms.EmailField()

	def clean_email2(self):
		# print("slime")
		email = self.cleaned_data["email"]
		email2 = self.cleaned_data.get("email2")
		print(self.cleaned_data)
		# print(email2)
		# print(email == email2)
		if email == email2:
			user_exist = User.objects.filter(email=email).count()
			if user_exist != 0:
				raise forms.ValidationError("User exists. Please login.")
			return email
		else:
			raise forms.ValidationError("Please Make Sure Emails are the same")

class AddressForm(forms.Form):
	billing_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(
		address_type="billing"),
		empty_label= None,
		widget= forms.RadioSelect,

	)
	shipping_address = forms.ModelChoiceField(queryset=UserAddress.objects.filter(
		address_type="shipping"),
		empty_label= None,
		widget= forms.RadioSelect,

	)
class UserAddressForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super(UserAddressForm, self).__init__(*args, **kwargs)
		self.helper = FormHelper()

	class Meta:
		model = UserAddress
		fields = [
			'street',
			'city',
			'state',
			'zipcode',
			'address_type'
		]