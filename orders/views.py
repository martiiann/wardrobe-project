from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = Order.objects.get(pk=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
