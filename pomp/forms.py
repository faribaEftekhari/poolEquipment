from django import forms
from . import models

class CreatePomp(forms.ModelForm):
    class Meta:
        model=models.pomps
        fields={'brand','modelnum','price','madein','discription','image'}
        labels={'brand':'برند','modelnum':'مدل','price':'قیمت','madein':'ساخت کشور','discription':'مشخصات کالا','image':'تصویر'}
