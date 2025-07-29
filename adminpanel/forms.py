from django import forms
from orders.models import Order
from products.models import Product, Size

class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status', 'tracking_number']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'tracking_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'category',
            'description',
            'price',
            'image',
            'is_available',
            'gender',
            'sizes',  
        ]
        widgets = {
            'sizes': forms.CheckboxSelectMultiple()
        }

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['name']        