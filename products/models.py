from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save, post_save
from django.utils.text import slugify
from django.utils.safestring import mark_safe 


# Create your models here.

class ProductQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

class ProductManager(models.Manager):
	def get_queryset(self):
		return ProductQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		return self.get_queryset().active()

	def get_related(self, instance):
		product = self.get_queryset().filter(categories__in=instance.categories.all())
		product_ = self.get_queryset().filter(default=instance.default)		
		qs = (product | product_).exclude(id=instance.id).distinct()
		return qs


class Product(models.Model):
	title = models.CharField(max_length = 30)
	slug = models.SlugField(blank=True)  #unique=True
	description = models.TextField()
	price = models.DecimalField(max_digits = 100, decimal_places = 2, default = 9.99)
	sales_price = models.DecimalField(max_digits = 100, decimal_places=2, default = 6.99, null=True, blank=True)
	active = models.BooleanField(default=True)
	categories = models.ManyToManyField('Category', blank=True)
	default = models.ForeignKey("Category", related_name='default_category', null=True, blank=True)
	# inventory 

	objects = ProductManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('product:detail', kwargs={'pk': self.pk})

	def get_image_url(self):
		img = self.productimage_set.first()
		if img:
			return img.image.url
		return img

class Variation(models.Model):
	product = models.ForeignKey(Product)
	title = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=100, decimal_places=2, default =9.99)
	sales_price = models.DecimalField(max_digits=100, decimal_places=2, default = 6.99, null=True, blank=True)
	active = models.BooleanField(default=True)
	inventory = models.IntegerField(null=True, blank=True )

	def __str__(self):
		return self.title

	def get_price(self):
		if self.sales_price is not None:
			return self.sales_price
		else:
			return self.price

	def get_html_price(self):
		if self.sales_price is not None:
			html_text = "<span class='sale-price'></span>{0}</span><span class='og-price'>{1}</span>".format(self.sales_price, self.price)
			return mark_safe(html_text)
		else:
			html_text = "<span class='price'></span>{0}</span>".format(self.price)
			return mark_safe(html_text)

	def get_absolute_url(self):
		return self.product.get_absolute_url()

	def add_to_cart(self):
		return "%s?item=%s&qty=1" %(reverse("cart:main"), self.id)

	def remove_from_cart(self):
		return "%s?item=%s&qty=1&delete=True" %(reverse("cart:main"), self.id)

	def get_title(self):
		return "%s - %s" %(self.product.title, self.title)


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

class Category(models.Model):
	title = models.CharField(max_length=120, unique=True)
	slug = models.SlugField(unique=True)
	description = models.TextField(blank=True, null=True)
	active = models.BooleanField(default=True)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('category:detail', kwargs={'slug': self.slug}) 