from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from . import models
from django.contrib.auth.models import User
class CreateUserForm(UserCreationForm):
    username=forms.CharField(max_length=30,min_length=5,label='نام کاربری')
    password1=forms.CharField(min_length=8,label='پسورد',widget=forms.PasswordInput)
    password2=forms.CharField(min_length=8,label='تکرار پسورد',widget=forms.PasswordInput)

class loginUserForm(forms.Form):
    username=forms.CharField(max_length=30,min_length=5,label='نام کاربری')
    password=forms.CharField(min_length=8,label='پسورد',widget=forms.PasswordInput)


class createUserCustomer(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        labels={'first_name':'نام','last_name':'نام خانوادگی','username':'نام کاربری','password':'پسورد'}
        widgets={
        'password': forms.PasswordInput()
        }
class customerPersonalForm(forms.ModelForm):
    class Meta:
        model=models.Customer
        fields=['isseller','isbuyer','mobile','address','image']
