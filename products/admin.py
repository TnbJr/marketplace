from django.contrib import admin
from .models import Product, Variation, ProductImage, Category
# Register your models here.


class ProductImageInline(admin.TabularInline):
	model = ProductImage
	extra = 0 

class VarationInline(admin.TabularInline):
	model = Variation
	extra = 0

class ProductAdmin(admin.ModelAdmin):
	list_display = ['__str__', 'price']
	inlines = [ ProductImageInline,
	VarationInline]
	class Meta:
		model = Product 

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation)
admin.site.register(ProductImage)
admin.site.register(Category)