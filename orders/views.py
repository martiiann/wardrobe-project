import stripe
import json
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if order.user != request.user:
        return HttpResponseForbidden("You do not have permission to view this order.")

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

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError as e:
        print("❌ JSON decode error:", e)
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    form = CheckoutForm(data)
    if not form.is_valid():
        print("❌ Form validation failed:", form.errors)
        return JsonResponse({'error': 'Invalid form data', 'details': form.errors}, status=400)

    # Stripe line items
    line_items = []
    cart_data = []

    for item in cart:
        size = item.get('size')

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item['product'].name,
                },
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

        cart_data.append({
            'product_id': item['product'].id,
            'product_name': item['product'].name,
            'quantity': item['quantity'],
            'price': str(item['price']),
            'size_id': size.id if hasattr(size, 'id') else '',
        })

    metadata = {
        'user_id': str(request.user.id),
        'email': form.cleaned_data['email'],
        'full_name': form.cleaned_data['full_name'],
        'address': form.cleaned_data['address'],
        'city': form.cleaned_data['city'],
        'postal_code': form.cleaned_data['postal_code'],
        'country': form.cleaned_data['country'],
        'payment_method': form.cleaned_data['payment_method'],
        'cart': json.dumps(cart_data),  # ✅ Send cart as JSON
    }

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/orders/success/'),
        cancel_url=request.build_absolute_uri('/cart/'),
        metadata=metadata,
    )

    return JsonResponse({'id': session.id})


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception as e:
        print("❌ Webhook signature verification failed:", e)
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        print("✅ Stripe session completed received")
        session = event['data']['object']
        metadata = session.get('metadata', {})
        print("📦 Metadata:", metadata)

        User = get_user_model()
        user = User.objects.filter(id=metadata.get('user_id')).first()

        if user:
            print("👤 User found:", user.email)

            # Create order
            order = Order.objects.create(
                user=user,
                full_name=metadata.get('full_name'),
                email=metadata.get('email'),
                address=metadata.get('address'),
                city=metadata.get('city'),
                postal_code=metadata.get('postal_code'),
                country=metadata.get('country'),
                payment_method=metadata.get('payment_method'),
                total_price=session['amount_total'] / 100,
            )
            print("🧾 Order created:", order.id)

            # ✅ Rebuild OrderItems from cart JSON
            try:
                from products.models import Product, Size
                from .models import OrderItem
                cart_items = json.loads(metadata.get('cart', '[]'))

                for item in cart_items:
                    product = Product.objects.get(id=item['product_id'])
                    size = Size.objects.get(id=item['size_id']) if item['size_id'] else None
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        size=size,
                        quantity=item['quantity'],
                        price=item['price'],
                    )
                print("📦 Order items saved.")
            except Exception as e:
                print("❌ Failed to create OrderItems:", e)

            # Build item summary for email
            items = order.items.all()
            item_lines = []
            for item in items:
                line = f"- {item.product.name} (x{item.quantity}) - ${item.price:.2f}"
                if item.size:
                    line += f" [Size: {item.size.name}]"
                item_lines.append(line)

            item_summary = "\n".join(item_lines)

            # Email body
            message = f"""Hi {user.first_name},

Thank you for your order #{order.id}!

Here’s what you ordered:
{item_summary}

Total: ${order.total_price:.2f}

We’ll notify you when your items are shipped.

Best regards,  
Wardrobe Team
"""

            try:
                send_mail(
                    subject="Order Confirmation",
                    message=message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[order.email],
                    fail_silently=False
                )
                print("📧 Email sent to:", order.email)
            except Exception as e:
                print("❌ Email sending failed:", e)
        else:
            print("❌ User not found from metadata user_id:", metadata.get('user_id'))

    return HttpResponse(status=200)

@login_required
def success(request):
    cart = Cart(request)
    cart.clear()
    messages.success(request, "Payment successful! Thank you for your order.")
    return render(request, 'orders/success.html')