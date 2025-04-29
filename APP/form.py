from django.contrib.auth.forms import UserCreationForm
from .models import User
from django import forms 
from .models import Seller  


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class SellerForm(forms.ModelForm): 
    class Meta:
        model = Seller
        fields = ['business_name','address','phone']