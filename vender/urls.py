from django.urls import include, path
from . import views
from accounts import views as ViewVendor

urlpatterns = [
    path(' ', ViewVendor.vendor_dashboard,  name = "vendor"),
    path("profile/", views.profile, name='vprofile'),
    
]   
