from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from .models import Profile

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 
				'date_of_birth',
				'gender',
				'cannabis_type',
				'location'
				 ]

class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			'username', 'email',
			'first_name', 'last_name'
		]

class UserCreateForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ['username', 'email']

	def save(self, commit=True):
		user = super(UserCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user


