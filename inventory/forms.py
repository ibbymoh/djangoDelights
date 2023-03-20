from django import forms
from .models import *

from django.contrib.auth.forms import UserCreationForm




class AddMenuItemForm(forms.ModelForm):

    class Meta:
        model = MenuItem
        fields = ["name","price"]
    name = forms.CharField()
    price = forms.FloatField()
