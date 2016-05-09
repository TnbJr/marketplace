from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify


# Create your models here.
class Product(models.Model):
	title = models.CharField(max_length=30)
	slug = models.SlugField(blank=True)  #unique=True
	description = models.TextField()
	price = models.DecimalField(max_digits=100, decimal_places=2, default =9.99)
	sales_price = models.DecimalField(max_digits=100, decimal_places=2, default = 6.99, null=True, blank=True)
	active = models.BooleanField(default=True)
	# inventory 

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product:detail', kwargs={'pk': self.pk})

class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=100, decimal_places=2, default =9.99)
	sales_price = models.DecimalField(max_digits=100, decimal_places=2, default = 6.99, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True )

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return self.product.get_absolute_url()

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)

def product_post_save_reciever(sender, instance, *args, **kwargs):
	product = instance 
	variation = product.variation_set.all()
	if variation.count() == 0:
		new_var = Variation()
		new_var.product = product
		new_var.title = "Default"
		new_var.price = product.price
		new_var.save()


pre_save.connect(product_pre_save_reciever, sender=Product)
post_save.connect(product_post_save_reciever, sender=Product)



class ProductImage(models.Model):
	product = models.ForeignKey(Product)
	image = models.ImageField(upload_to='products/')

	def __str__(self):
		return self.product.title