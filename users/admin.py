from django.contrib import admin
from .models import Profile

# class UserReviewAdmin(admin.ModelAdmin):
# 	model = UserReview
	
admin.site.register(Profile)
