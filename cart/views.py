from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product
from .cart import Cart
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import get_messages

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        size_id = request.POST.get('size')  # ✅ Read size from POST
        size_obj = None
        if size_id:
            try:
                size_obj = Size.objects.get(id=size_id)
            except Size.DoesNotExist:
                size_obj = None

        if quantity > 0:
            cart.add(product, size_obj, quantity)  # ✅ Pass Size object
            messages.success(request, f"{product.name} (Size: {size_obj.name if size_obj else 'Not specified'}) added to cart.")
        else:
            cart.remove(product, size_obj)
            messages.info(request, f"{product.name} removed from cart.")

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