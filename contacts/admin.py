from django.contrib import admin
from .models import Contact
# Register your models here.
class ContactAdmin(admin.ModelAdmin):
	list_display = ['timestamp', 'name', 'email']
	list_display_links = ["name"]
	list_filter = ["timestamp"]
	
	class Meta:
		model = Contact

admin.site.register(Contact, ContactAdmin)