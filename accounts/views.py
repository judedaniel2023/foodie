from django.shortcuts import render, redirect
from accounts.forms import UserForm
from accounts.models import User, UserProfile
from django.contrib import messages
from django.contrib import auth
from .utils import detectUser, send_password_reset_email
from django.contrib.auth.decorators import login_required, user_passes_test
from .utils import send_verification_email
from vender.forms import VendorForm
from django.core.exceptions import PermissionDenied
from django.utils.http import  urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator 
from  vender.models import Vender

def check_role_vendor(user):
    if user.role == 1:
        return True
    else:
        raise PermissionDenied
    
def check_role_customer(user):
    if user.role == 2:
        return True
    else:
        raise PermissionDenied
    

# Create your views here.
def registerUser(request):
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

            send_verification_email(request, user)
            messages.success(request, "Account created successfully")
            return redirect('registerUser')
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

            send_verification_email(request, user)
            messages.success(request, "Account created successfully, check your email to activate your account")
            return redirect('registerVendor')
        else:
            print("Either form not valid")
    else:
        form = UserForm()
        v_form = VendorForm()
   
    return render(request, 'accounts/register_vendor.html', {'form': form, 'v_form': v_form})



def login(request):
    if request.user.is_authenticated:
       return redirect('my_account')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request,"Login successfully")
            return redirect('my_account')
        else:
            messages.error(request, "Login credentials are wrong")
            return redirect('login')
    return render(request, 'accounts/login.html')


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    messages.info(request, "Logout successful")
    return redirect('login')


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer_dashboard(request):
    # if request.user.get_role() is not 'Customer':
    #     messages.error(request, 'Permision denied')
    #     return redirect('my_account')  
    return render(request, 'accounts/customer_dashboard.html')


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vendor_dashboard(request):
    vendor = Vender.objects.get(user = request.user)
    context = {
        'vendor': vendor
    }
    return render(request, 'accounts/vendor_dashboard.html', context)

@login_required(login_url='login')
def my_account(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


def activate(request, uidb64, token):
    # ativate the user by setting the is_activate status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Congratulation! Your account is activated")
        return redirect('my_account')
    else:
        messages.error(request, 'Invalid activateion link')
        return redirect('my_account')
    

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email__exact=email)
            #send reset password email
            send_password_reset_email(request, user)
            messages.success(request, "Password reset link has been sent to your email address")
            return redirect('forgot_password')
        else:
            messages.error(request, 'Account does not exist')
            return redirect('forgot_password')
    return render(request, 'accounts/forgot_password.html')


def reset_password_validate(request, uidb64, token):
    # ativate the user by setting the is_activate status to true
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User._default_manager.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('reset_password')
    else:
        messages.error(request, 'This link has expired')
        return redirect('my_accounts')

def reset_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_passord = request.POST['confirm_password']
        if password == confirm_passord:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Password reset successful')
            return redirect('login')
        else:
            messages.error(request, 'Password do not match!')
            return redirect('reset_password')

    return render(request, 'accounts/emails/reset_password.html')