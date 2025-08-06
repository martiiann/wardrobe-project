import json
import secrets
import stripe
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail
from django.http import (
    HttpResponse,
    JsonResponse,
    HttpResponseForbidden,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .forms import CheckoutForm
from .models import Order, OrderItem
from cart.cart import Cart


stripe.api_key = settings.STRIPE_SECRET_KEY

# Confirmed working during TDD process
def order_history(request):
    if not request.user.is_authenticated:
        return redirect('login')
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.GET.get('just_ordered') == 'true':
        messages.success(
            request,
            f"Your order #{order.id} has been placed successfully!"
        )

    if order.user and request.user.is_authenticated:
        if order.user != request.user:
            return HttpResponseForbidden(
                "You do not have permission to view this order."
            )
    elif not order.user:
        token = request.GET.get('token')
        if not token or str(token) != str(order.guest_token):
            return HttpResponseForbidden(
                "You do not have permission to view this order."
            )

    return render(request, 'orders/order_detail.html', {'order': order})


def guest_order_detail(request, order_id, token):
    order = get_object_or_404(
        Order,
        id=order_id,
        guest_token=token,
        user__isnull=True
    )

    if request.GET.get('just_ordered') == 'true':
        messages.success(
            request,
            f"Your order #{order.id} has been placed successfully!"
        )

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

            if request.user.is_authenticated:
                order.user = request.user
            else:
                order.user = None
                order.guest_token = uuid.uuid4()

            order.email = form.cleaned_data.get('email')
            order.full_name = form.cleaned_data.get('full_name')
            order.total_price = cart.get_total_price()
            order.save()

            from products.models import Size
            for item in cart:
                size_obj = None
                size_id = getattr(
                    item.get('size_obj'),
                    'id',
                    item.get('size_id')
                )

                print(
                    "DEBUG Checkout item:",
                    item['product'],
                    "size_id:", size_id,
                    "size_name:", getattr(item.get('size_obj'), 'name', None)
                )

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

            if order.guest_token:
                request.session['guest_order_token'] = str(order.guest_token)

            cart.clear()
            messages.success(request, "Your order has been placed!")

            if order.user:
                return redirect('orders:order_detail', order.id)
            else:
                return redirect(
                    f"{order.get_guest_order_url()}?token={order.guest_token}"
                    "&just_ordered=true"
                )
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
        return JsonResponse(
            {'error': 'Invalid form data', 'details': form.errors},
            status=400
        )

    order = form.save(commit=False)
    if request.user.is_authenticated:
        order.user = request.user
    else:
        order.user = None
        order.guest_token = secrets.token_urlsafe(16)

    order.email = form.cleaned_data['email']
    order.full_name = form.cleaned_data['full_name']
    order.total_price = cart.get_total_price()
    order.status = 'Pending'
    order.save()

    from products.models import Size
    for item in cart:
        size_obj = None
        size_id = getattr(item.get('size_obj'), 'id', item.get('size_id'))
        if size_id:
            try:
                size_obj = Size.objects.get(id=size_id)
            except Size.DoesNotExist:
                pass

        OrderItem.objects.create(
            order=order,
            product=item['product'],
            size=size_obj,
            quantity=item['quantity'],
            price=item['price']
        )

    if order.guest_token:
        request.session['guest_order_token'] = str(order.guest_token)

    delivery_fee = cart.get_delivery_fee()
    line_items = []

    for item in cart:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': item['product'].name},
                'unit_amount': int(item['price'] * 100),
            },
            'quantity': item['quantity'],
        })

    if delivery_fee > 0:
        line_items.append({
            'price_data': {
                'currency': 'eur',
                'product_data': {'name': 'Delivery Fee'},
                'unit_amount': int(delivery_fee * 100),
            },
            'quantity': 1,
        })

    metadata = {
        'order_id': str(order.id),
        'guest_token': order.guest_token or '',
        'user_id': str(order.user.id) if order.user else '',
    }

    success_url = request.build_absolute_uri(
        '/orders/success/'
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(reverse('orders:cancelled'))

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
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        metadata = session.get('metadata', {})

        User = get_user_model()
        user = User.objects.filter(id=metadata.get('user_id')).first() if metadata.get('user_id') else None

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
            status='Pending',  # 👈 Keep it as Pending until you manually update it
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

        site_url = settings.SITE_URL if hasattr(settings, 'SITE_URL') else request.build_absolute_uri('/')

        # Correct URL based on user type
        order_url = (
            f"{site_url}orders/{order.id}/"
            if order.user
            else f"{site_url}orders/guest/{order.id}/{order.guest_token}/"
        )

        # ✅ Build email-safe items with full image URLs
        email_items = []
        for item in order.items.all():
            image_url_full = f"{site_url}{item.product.image.url}" if item.product.image else ''
            email_items.append({
                'product_name': item.product.name,
                'image_url_full': image_url_full,
                'size': item.size.name if item.size else '-',
                'quantity': item.quantity,
                'price': item.price,
            })

        # ✅ Render HTML email
        html_message = render_to_string(
            'orders/email_confirmation.html',
            {
                'order': order,
                'items': email_items,
                'order_url': order_url,
                'site_url': site_url,
            }
        )

        # ✅ Send email to user
        email = EmailMultiAlternatives(
            subject=f"Order Confirmation #{order.id}",
            body=f"Thank you for your order #{order.id}. View here: {order_url}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.email],
        )
        email.attach_alternative(html_message, "text/html")
        email.send(fail_silently=False)

        # ✅ Send admin notification
        send_mail(
            subject=f"New Order #{order.id} Placed",
            message=(
                f"A new order has been placed.\n\n"
                f"Order ID: {order.id}\n"
                f"Customer: {order.full_name}\n"
                f"Total: £{order.total_price:.2f}\n"
                f"View: {order_url}"
            ),
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
        order_id = metadata.get('order_id')

        order = None
        if order_id:
            order = Order.objects.filter(id=order_id).first()

        if order:
            if order.user:
                order_url = reverse('orders:order_detail', args=[order.id])
            else:
                order_url = order.get_guest_order_url()

            separator = '&' if '?' in order_url else '?'
            return redirect(f"{order_url}{separator}just_ordered=true")

    messages.warning(
        request,
        "We couldn’t find your order, but your payment may have gone through. Please check your email."
    )
    return redirect('shop')
