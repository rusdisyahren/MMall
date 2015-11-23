from django import forms
from ecommerce.models import Product

class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['title', 'picture', 'price', 'brand', 'category']