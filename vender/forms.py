from django import forms

from vender.models import Vender


class VendorForm(forms.ModelForm):
    class Meta:
        model = Vender
        fields = ['vendor_name', 'vendor_license']