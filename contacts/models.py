from django.db import models

# Create your models here.
class Contact(models.Model):
	name = models.CharField(max_length=120)
	subject = models.CharField(max_length=255)
	email = models.EmailField()
	message = models.TextField()
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)
	
	def __str__(self):
		return self.email