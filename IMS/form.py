from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Data, Delivery

class DataForm(forms.ModelForm):

    class Meta:
        model = Data
        fields = ('install_date', 'serial', 'hostname', 'status', 'place', 'vendor', 'location', 'part', 'description', 'next_serial' )
        labels = {
            'install_date': _('설치일'),
        }

class DeliveryForm(forms.ModelForm, forms.Form):
    class Meta:
        model = Delivery
        fields = ('rma_num', 'serial', 'part', 'status', 'vendor')
