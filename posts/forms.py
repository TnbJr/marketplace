from django import forms
from .models import ContentPost

class ContentPostForm(forms.ModelForm):
	class Meta:
		model = ContentPost
		fields = ['title',
				'image',
				 'content',
				 'draft',
				 'published',
				 'categories',
				 'source',
			 ]