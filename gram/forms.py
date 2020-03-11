from django import forms
from .models import Image,Profile,Comment,Signup
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class NewImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['pub_date','profile']


class ProfileUpdateForm(forms.Form):
    '''
    classs that creates profile update form
    '''
    username = forms.CharField(label='Username',max_length = 30)
    profile_photo = forms.ImageField(label = 'Image Field')
    bio = forms.CharField(label='Image Caption',max_length=500)

class CommentForm(forms.ModelForm):
    '''
    class that creates the comment form
    '''
    class Meta:
        model = Comment
        fields = ['comment']

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model=User
        fields=['username','email','password1','password2']

