from django import forms
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
