from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id, size=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart.add(product, size, quantity)
        else:
            # Handle quantity reduction
            key = cart._generate_key(product.id, size)
            current_qty = cart.cart.get(key, {}).get('quantity', 0)
            new_qty = max(0, current_qty + quantity)
            
            if new_qty > 0:
                cart.add(product, size, quantity)
            else:
                cart.remove(product, size)
    
    return redirect('cart:detail')

def cart_remove(request, product_id, size=None):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    cart.remove(product, size)
    messages.success(request, f"{product.name} was removed from your cart.")
    
    return redirect('cart:detail')

def cart_update(request, product_id, size=None):
    """Handle direct quantity updates"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product, size, quantity, override_quantity=True)
    
    return redirect('cart:detail')