from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# from django.conf.settings import AUTH_USER_MODEL as User

from .models import Category, Comment, Post, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter username...'})
        self.fields['password1'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Enter password...'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Confirm password...'})



class AddPost(forms.ModelForm):
     class Meta:
         model = Post
         fields = ('title', 'category', 'content', 'tag', 'image')
         labels = {
             'title': '',
             'category': 'Category',
             'content': '',
             'tag': 'Tag',
             'image': '',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
             'category': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Choose Category...'}),
             'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Content...'}),
             'tag': forms.SelectMultiple(attrs={'class': 'form-select', 'placeholder': 'Choose Tag...'}),
         }


class AddCategory(forms.ModelForm):
     class Meta:
         model = Category
         fields = ('title', 'parent')
         labels = {
             'title': '',
             'parent': 'Parent',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
             'parent': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose Parent...'}),
         }


class AddTag(forms.ModelForm):
     class Meta:
         model = Tag
         fields = ('title', )
         labels = {
             'title': '',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
         }


class AddComment(forms.ModelForm):
     class Meta:
         model = Comment
         fields = ('title', 'content')
         labels = {
             'title': '',
             'content': '',
         }
         widgets = {
             'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Title...'}),
             'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter Content...'}),
         }
