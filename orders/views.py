import stripe
import json
import secrets
import uuid
from django.http import HttpResponse, JsonResponse, HttpResponseForbidden
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import get_user_model
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.cart import Cart
from django.template.loader import render_to_string
from django.urls import reverse
from django.core.mail import send_mail

stripe.api_key = settings.STRIPE_SECRET_KEY


def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # 🔹 Show success message if redirected right after checkout
    if request.GET.get('just_ordered') == 'true':
        messages.success(request, f"Your order #{order.id} has been placed successfully!")

    # Usual permission checks...
    if order.user and request.user.is_authenticated:
        if order.user != request.user:
            return HttpResponseForbidden("You do not have permission to view this order.")
    elif not order.user:
        token = request.GET.get('token')
        if not token or str(token) != str(order.guest_token):
            return HttpResponseForbidden("You do not have permission to view this order.")

    return render(request, 'orders/order_detail.html', {'order': order})


from django.conf import settings

def guest_order_detail(request, order_id, token):
    order = get_object_or_404(Order, id=order_id, guest_token=token, user__isnull=True)

    # Show success message after checkout
    if request.GET.get('just_ordered') == 'true':
        messages.success(request, f"Your order #{order.id} has been placed successfully!")

    return render(request, 'orders/order_detail.html', {'order': order})

def checkout(request):
    cart = Cart(request)

    if not cart:
        messages.warning(request, "Your cart is empty.")
        return redirect('shop')

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            # Logged in user or guest
            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = None
                order.guest_token = uuid.uuid4()

            order.email = form.cleaned_data.get('email')
            order.full_name = form.cleaned_data.get('full_name')
            order.total_price = cart.get_total_price()
            order.save()

            # ✅ Create order items with correct Size instance
            from products.models import Size
            for item in cart:
                size_obj = None
                size_id = getattr(item.get('size_obj'), 'id', item.get('size_id'))

                # 🔍 Debug line to see what checkout receives
                print("DEBUG Checkout item:",
                    item['product'],
                    "size_id:", size_id,
                    "size_name:", getattr(item.get('size_obj'), 'name', None))

                if size_id:
                    try:
                        size_obj = Size.objects.get(id=size_id)
                    except Size.DoesNotExist:
                        size_obj = None

                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    size=size_obj,
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Store guest token in session for redirect
            if order.guest_token:
                request.session['guest_order_token'] = str(order.guest_token)

            # Clear cart
            cart.clear()

            messages.success(request, "Your order has been placed!")
            if order.user:
                return redirect('orders:order_detail', order.id)
            else:
                return redirect(f"{order.get_guest_order_url()}?token={order.guest_token}&just_ordered=true")
    else:
        form = CheckoutForm()

    return render(request, 'orders/checkout.html', {'form': form})

@csrf_exempt
def create_checkout_session(request):
    cart = Cart(request)
    if not cart:
        return JsonResponse({'error': 'Cart is empty'}, status=400)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    form = CheckoutForm(data)
    if not form.is_valid():
        return JsonResponse({'error': 'Invalid form data', 'details': form.errors}, status=400)

    line_items = []
    cart_data = []
    for item in cart:
        size_id = getattr(item.get('size_obj'), 'id', item.get('size_id'))

        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': item['product'].name},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })
        cart_data.append({
            'product_id': item['product'].id,
            'quantity': item['quantity'],
            'price': str(item['price']),
            'size_id': size_id if size_id else '',
        })

    guest_token = ''
    user_id = ''
    if request.user.is_authenticated:
        user_id = str(request.user.id)
    else:
        guest_token = secrets.token_urlsafe(16)

    metadata = {
        'user_id': user_id,
        'guest_token': guest_token,
        'email': form.cleaned_data['email'],
        'full_name': form.cleaned_data['full_name'],
        'address': form.cleaned_data['address'],
        'city': form.cleaned_data['city'],
        'postal_code': form.cleaned_data['postal_code'],
        'country': form.cleaned_data['country'],
        'payment_method': form.cleaned_data['payment_method'],
        'cart': json.dumps(cart_data),
    }

    success_url = request.build_absolute_uri('/orders/success/') + "?session_id={CHECKOUT_SESSION_ID}"
    cancel_url = request.build_absolute_uri('/cart/')

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata=metadata,
    )

    return JsonResponse({'id': session.id})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        User = get_user_model()
        user = User.objects.filter(id=metadata.get('user_id')).first() if metadata.get('user_id') else None

        # Create order
        order = Order.objects.create(
            user=user,
            guest_token=metadata.get('guest_token') if not user else None,
            full_name=metadata.get('full_name', 'Guest'),
            email=metadata.get('email', ''),
            address=metadata.get('address', ''),
            city=metadata.get('city', ''),
            postal_code=metadata.get('postal_code', ''),
            country=metadata.get('country', ''),
            payment_method=metadata.get('payment_method', 'card'),
            total_price=session['amount_total'] / 100,
        )

        from products.models import Product, Size
        cart_items = json.loads(metadata.get('cart', '[]'))
        for item in cart_items:
            size = None
            if item.get('size_id'):
                try:
                    size = Size.objects.get(id=item['size_id'])
                except Size.DoesNotExist:
                    size = None

            product = Product.objects.get(id=item['product_id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                size=size,
                quantity=item['quantity'],
                price=item['price'],
            )

        # Email confirmation
        site_url = settings.SITE_URL if hasattr(settings, 'SITE_URL') else request.build_absolute_uri('/')
        order_url = f"{site_url}orders/{order.id}/"
        if order.guest_token:
            order_url += f"?token={order.guest_token}"

        html_message = render_to_string('orders/email_confirmation.html', {
            'order': order,
            'items': order.items.all(),
            'order_url': order_url,
            'site_url': site_url,  # For absolute image URLs
        })

        email = EmailMultiAlternatives(
            subject=f"Order Confirmation #{order.id}",
            body=f"Thank you for your order #{order.id}. View here: {order_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send()

        # Email notification to admin
        admin_email = settings.DEFAULT_FROM_EMAIL  # or a dedicated admin address if you have one
        send_mail(
            subject=f"New Order #{order.id} Placed",
            message=f"A new order has been placed.\n\nOrder ID: {order.id}\nCustomer: {order.full_name}\nTotal: £{order.total_price}\nView: {order_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            fail_silently=False,
        )
    return HttpResponse(status=200)

def success(request):
    cart = Cart(request)
    cart.clear()

    session_id = request.GET.get('session_id')
    if session_id:
        stripe_session = stripe.checkout.Session.retrieve(session_id)
        metadata = stripe_session.get('metadata', {})
        user_id = metadata.get('user_id')
        guest_token = metadata.get('guest_token')

        order = Order.objects.filter(
            user_id=user_id if user_id else None,
            guest_token=guest_token if guest_token else None
        ).order_by('-created_at').first()

        if order:
            if order.user:
                return redirect(f"{reverse('orders:order_detail', args=[order.id])}?just_ordered=true")
            else:
                return redirect(f"{order.get_guest_order_url()}?token={order.guest_token}&just_ordered=true")

    return redirect('home')