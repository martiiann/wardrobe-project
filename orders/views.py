from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.cart import Cart

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def checkout(request):
    cart = Cart(request)

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_price = cart.get_total_price()
            order.save()

            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=item.get('size'),
                    price=item['price'],
                    quantity=item['quantity']
                )

            cart.clear()
            messages.success(request, "Your order has been placed!")
            return redirect('order_detail', order.id)
    else:
        # Pre-fill form from saved profile, if available
        profile = getattr(request.user, 'profile', None)
        initial_data = {}
        if profile:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'address': profile.address,
                'city': profile.city,
                'postal_code': profile.postal_code,
                'country': profile.country,
                'payment_method': profile.payment_method,
            }
        form = CheckoutForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {'form': form})