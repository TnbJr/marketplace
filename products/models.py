from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
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

def product_pre_save_reciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = slugify(instance.title)


pre_save.connect(product_pre_save_reciever, sender=Product)