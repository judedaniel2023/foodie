from django.db import models

from accounts.models import User, UserProfile
from accounts.utils import send_notification_email

# Create your models here.
class Vender(models.Model):
    user = models.OneToOneField(User, related_name="user", on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name="user_profile", on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    vendor_license = models.ImageField(upload_to="vender/license")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)



    def __str__(self) :
        return self.vendor_name
    

    def save(self, *args, **kwargs):
        if self.pk is not None:
             #Update
                orig = Vender.objects.get(pk=self.pk)
                if orig.is_approved != self.is_approved:
                    mail_template = "accounts/emails/admin_approval_email.html"
                    context = {
                             'user':self.user,
                             'is_approved':self.is_approved,
                     }
                    if self.is_approved == True:      
                        #Send notification email   
                        mail_subject = "Congratulations! You have successfully"
                        send_notification_email(mail_subject, mail_template, context)
                    else:
                        mail_subject = "We're sorry! You are not eligible for publishng your food menu on our website"
                        send_notification_email(mail_subject, mail_template, context) 

        return super(Vender, self).save(*args, **kwargs)

                   
            

             