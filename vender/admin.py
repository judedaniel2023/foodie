from django.contrib import admin

from vender.models import Vender

# Register your models here.

class VendorAdmin(admin.ModelAdmin):
    list_display = ('user', 'vendor_name', 'is_approved', 'created_at')
    list_display_links = ('user', 'vendor_name')
admin.site.register(Vender, VendorAdmin)