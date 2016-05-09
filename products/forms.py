from django import forms
from .models import Product



# class ProductAddForm(forms.Form):
# 	title = forms.CharField(label='Product Name')
# 	description = forms.CharField(widget=forms.Textarea(
# 		attrs ={
# 		"class": "han",
# 		"placeholder": "description",
# 		}
# 		))
# 	price = forms.DecimalField()


# 	def clean_price(self):
# 		price = self.cleaned_data.get("price")
# 		if price <= 1.00:
# 			raise forms.ValidationError("Price must be greater than $1.00")
# 		elif price >= 99.99:
# 			raise forms.ValidationError("Prce must be less than $100.00 ")
# 		else:
# 			return price

# 	def clean_title(self):
# 		title = self.cleaned_data.get("title")
# 		if len(title) < 3:
# 			raise forms.ValidationError("Title must be more then three characters")
# 		else:
# 			return title

class ProductModelForm(forms.ModelForm):
	class Meta:
		model = Product
		fields = [
			"title",
			"description",
			"price"
		]

		widgets = { "description": forms.Textarea(
						attrs={
							"placeholder": "New Description"
						}
			)}

	def clean_price(self):
		price = self.cleaned_data.get("price")
		if price <= 1.00:
			raise forms.ValidationError("Price must be greater than $1.00")
		elif price >= 99.99:
			raise forms.ValidationError("Prce must be less than $100.00 ")
		else:
			return price

	def clean_title(self):
		title = self.cleaned_data.get("title")
		if len(title) < 3:
			raise forms.ValidationError("Title must be more then three characters")
		else:
			return title