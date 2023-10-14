from django.urls import include, path
from . import views


urlpatterns = [
    path('', views.my_account),
    path("registerUser/", views.registerUser, name='registerUser'),
    path("registerVendor/", views.registerVendor, name='registerVendor'),

    
    path("login/", views.login, name='login'),
    path("logout/", views.logout, name='logout'),
    path("vendor_dashboard/", views.vendor_dashboard, name='vendor_dashboard'),
    path("customer_dashboard/", views.customer_dashboard, name='customer_dashboard'),
    path("my_account", views.my_account, name='my_account'),
    path("activate/<uidb64>/<token>/", views.activate, name='activate'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/', views.reset_password, name = "reset_password"),
    path('vendor/', include('vender.urls')),
    
]   
