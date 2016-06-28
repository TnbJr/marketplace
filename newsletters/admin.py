from django.contrib import admin
from .models import SignUp
from .forms import SignUpForm
# Register your models here.
class SignUpAdmin(admin.ModelAdmin):
	list_display = ["email", "timestamp"]
	list_display_links = ["email"]
	list_filter = ["timestamp", "email"]
	
	class Meta:
		model = SignUp


admin.site.register(SignUp, SignUpAdmin)