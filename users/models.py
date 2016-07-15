from django.db import models
from django.dispatch import receiver 
# from allauth.account.signals import user_signed_up
from django.contrib.auth.models import User

class Profile(models.Model):
	GENDER_CHOICES = (
		("Male", "M"),
		("Female", "F"),
		("N/A", "Does it really matter?"),
		)
	WEED_CHOICES = (
		("Sativa", "Sativa"),
		("Indica", "Indica"),
		("Hybrid", "Hybrid"),
		)
	user = models.OneToOneField(User, related_name="profile")
	bio = models.TextField(blank=True, null=True)
	date_of_birth = models.DateField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	gender = models.CharField(max_length=50, choices=GENDER_CHOICES, default="M", blank=True, null=True)
	cannabis_type = models.CharField(max_length=50, choices=WEED_CHOICES, default="Sativa", blank=True, null=True)
	location = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__(self):
		return str(self.user)

	# @receiver(user_signed_up, sender=User)
	# def user_signed_up(request, user, *args, **kwargs):
	# 	if user:
	# 		profile = Profile.objects.get_or_create(user=user)

	
