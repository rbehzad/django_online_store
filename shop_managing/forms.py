from os import stat
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


class CreateTagForm(forms.ModelForm):
     class Meta:
         model = Tag
         fields = ('title',)
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
         }


class AddProductForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super (AddProductForm, self ).__init__(*args, **kwargs)
        self.fields['shop'].queryset = Shop.objects.filter(user=user).filter(status='Confirmed')

    class Meta:
        model = Product
        fields = ('title', 'description', 'price', 'tag', 'shop', 'amount', 'image')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Description...'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Price...'}),
            'tag': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Choose Tag...'}),
            'shop': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Shop...'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount...'}),
        }