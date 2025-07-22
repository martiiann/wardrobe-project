import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
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

stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
@csrf_exempt
def create_checkout_session(request):
    cart = Cart(request)

    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    line_items = []
    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['product'].name,
                },
                'unit_amount': int(item['price'] * 100),  # Stripe uses cents
            },
            'quantity': item['quantity'],
        })

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/orders/success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
    )

    return JsonResponse({'id': session.id})

@login_required
def success(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Payment successful! Thank you for your order.")
    return render(request, 'orders/success.html')
