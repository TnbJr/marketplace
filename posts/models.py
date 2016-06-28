from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify 
from django.utils import timezone 
# from taggit.managers import TaggableManager



class ContentPost(models.Model):
	CATEGORY_CHOICES = (
		("news", "News"),
		("entertainmet", "Entertainmet"),
		("other", "Other"),
		)
	title = models.CharField(max_length=255, unique=True)
	slug = models.SlugField()
	image = models.ImageField(null=True, blank=True)
	content = models.TextField()
	source = models.URLField(null=True, blank=True)
	# tags = TaggableManager() 
	draft = models.BooleanField(default=False)
	published = models.DateTimeField(auto_now=False, auto_now_add=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	categories = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="Entertainmet") 
	

	def __str__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("post:detail", kwargs={"slug": self.slug})


	def get_section_url(self):
		return reverse("post:detail-category", kwargs={"slug": self.categories})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.title)
			super().save(*args, **kwargs)
		else:
			super().save(*args, **kwargs)

	class Meta:
		ordering = ['-created']
