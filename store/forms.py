from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Customer, Order, Product

class CustomerRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm-Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class LoginForm(forms.Form):
    # email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'address', 'phone', 'image']

class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "__all__"

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
