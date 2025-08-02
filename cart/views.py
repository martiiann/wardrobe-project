from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product, Size
from .cart import Cart
from django.contrib import messages
from django.http import JsonResponse

def cart_detail(request):
    """Display the contents of the cart"""
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        change = int(request.POST.get('quantity', 1))

        size_id = request.POST.get('size')
        size_obj = None
        if size_id:
            try:
                size_obj = Size.objects.get(id=size_id)
            except Size.DoesNotExist:
                size_obj = None

        current_qty = cart.get_product_quantity(product, size_obj)
        new_qty = current_qty + change

        if new_qty > 0:
            cart.add(product, size_obj, new_qty, override_quantity=True)
        else:
            cart.remove(product, size_obj)

        # ✅ AJAX response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            updated_qty = cart.get_product_quantity(product, size_obj)
            return JsonResponse({
                'status': 'success',
                'name': product.name,
                'image': product.image.url if product.image else '',
                'price': float(product.get_current_price()),  # unit price
                'item_quantity': updated_qty,  # ✅ for table quantity update
                'item_total_price': float(product.get_current_price() * updated_qty),  # ✅ for subtotal update
                'size': size_obj.name if size_obj else None,
                'cart_total_price': float(cart.get_total_price()),
                'cart_total_items': len(cart),
                'cart_count': cart.count(),
            })

    return redirect('cart:detail')

def cart_remove(request, product_id, size=None):
    """Remove a product (with size) from the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    size_obj = None
    if size:
        try:
            size_obj = Size.objects.get(id=size)
        except Size.DoesNotExist:
            size_obj = None

    cart.remove(product, size_obj)

    message = f"{product.name} (Size: {size_obj.name if size_obj else 'Not specified'}) removed from cart."

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'status': 'success',
            'message': message,
            'cart_total_price': cart.get_total_price(),
            'cart_total_items': len(cart),
            'cart_count': cart.count(),
        })

    messages.success(request, message)
    return redirect('cart:detail')

def cart_update(request, product_id, size=None):
    """Update quantity of a product in the cart"""
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    size_obj = None
    if size:
        try:
            size_obj = Size.objects.get(id=size)
        except Size.DoesNotExist:
            size_obj = None

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart.add(product, size_obj, quantity, override_quantity=True)
    
    return redirect('cart:detail')