from django import forms
from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'full_name',
            'email',
            'address',
            'city',
            'postal_code',
            'country',
            'payment_method'
        ]
        widgets = {
            'full_name': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'email': forms.EmailInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'address': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'city': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'postal_code': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'country': forms.TextInput(
                attrs={'class': 'form-control bg-dark text-white'}
            ),
            'payment_method': forms.Select(
                attrs={'class': 'form-select bg-dark text-white'}
            ),
        }
