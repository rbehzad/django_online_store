from django import forms
from .models import *


class CreateShopForm(forms.ModelForm):
     class Meta:
         model = Shop
         fields = ('title', 'shop_type',)
         labels = {
             'title': '',
             'shop_type': 'Shop Type',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
             'shop_type': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Shop Type...'}),
         }