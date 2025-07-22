from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'address', 'city', 'postal_code', 'country', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'payment_method': forms.Select(attrs={'class': 'form-select'}),
        }
