from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages

from vender.forms import VendorForm

# Create your views here.
def registerUser(request):
    print("Congratulations! You have registered")
    if request.method == 'POST':
       form = UserForm(request.POST)
       if form.is_valid():
            # password = form.cleaned_data['password']
            # user = form.save(commit=False)
            # user.role = User.CUSTOMER
            # user.set_password(password)
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password= form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.CUSTOMER
            user.save()
            messages.error(request, "Account created successfully")
            return HttpResponseRedirect(request.path_info)
       else:
            print("InValide errors")
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'accounts/register_user.html', {'form': form})
                  
                  
                  
                  
                  

def registerVendor(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        v_form = VendorForm(request.POST, request.FILES)  
        if form.is_valid() and v_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password= form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username, email=email, password=password)
            user.role = User.VENDOR
            user.save()

            vendor = v_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, "You account has been registered successfully created")
            return redirect('registerVendor')
        else:
            print("Either form not valid")
    else:
        form = UserForm()
        v_form = VendorForm()
   
    return render(request, 'accounts/register_vendor.html', {'form': form, 'v_form': v_form})