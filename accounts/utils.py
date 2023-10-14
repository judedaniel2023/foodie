from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings



def detectUser(user):
    if user.role == 1:
        redirectUrl = "vendor_dashboard"
        return redirectUrl
    elif user.role == 2:
        redirectUrl = "customer_dashboard"
        return redirectUrl
    elif user.role == None and user.is_superadmin:
        redirectUrl = "/admin"
        return redirectUrl
    



def send_verification_email(request, user):
    current_site = get_current_site(request)
    mail_subject = "Please activate your account"
    message = render_to_string("accounts/emails/account_verification_email.html",  {
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    to_email = user.email
    send_mail(mail_subject,message ,settings.DEFAULT_FROM_EMAIL, [to_email, "danieljude799@gmail.com"], fail_silently=False)


# def send_verification_email(request, user):
#     subject = "Please activate your account"
#     message = "Hi Thank you for registering"
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [user.email,]
#     send_mail(subject,message, email_from, recipient_list)
def send_password_reset_email(request, user):
    current_site = get_current_site(request)
    mail_subject = "Reset Your Password"
    message = render_to_string("accounts/emails/reset_password_email.html",  {
        'user':user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    })

    to_email = user.email
    send_mail(mail_subject,message ,settings.DEFAULT_FROM_EMAIL, [to_email, "danieljude799@gmail.com"], fail_silently=False)



def send_notification_email(mail_subject, mail_template, context):
    from_email = settings.DEFAULT_FROM_EMAIL
    message = render_to_string(mail_template, context)
    to_email = context["user"].email
    send_mail(mail_subject, message, from_email, [to_email])
