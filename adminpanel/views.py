from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Size
from .forms import ProductForm, SizeForm
from orders.models import Order
from .forms import OrderUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

# ✅ Unified admin check
def admin_required(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_required)
def dashboard(request):
    return redirect('adminpanel:admin_order_list')

@login_required
@user_passes_test(admin_required)
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'adminpanel/order_list.html', {'orders': orders})

@login_required
@user_passes_test(admin_required)
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderUpdateForm(request.POST or None, instance=order)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Order updated successfully!')
        return redirect('adminpanel:admin_order_detail', order_id=order.id)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
        'form': form,
    })

@login_required
@user_passes_test(admin_required)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})

@login_required
@user_passes_test(admin_required)
def product_edit(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product saved successfully!')
            return redirect('adminpanel:product_list')
    else:
        form = ProductForm(instance=product)

    return render(request, 'adminpanel/product_form.html', {
        'form': form,
        'product': product
    })

@login_required
@user_passes_test(admin_required)
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted.')
    return redirect('adminpanel:product_list')

@login_required
@user_passes_test(admin_required)
def size_list(request):
    sizes = Size.objects.all()
    return render(request, 'adminpanel/size_list.html', {'sizes': sizes})

@login_required
@user_passes_test(admin_required)
def size_form(request, size_id=None):
    size = get_object_or_404(Size, id=size_id) if size_id else None
    if request.method == 'POST':
        form = SizeForm(request.POST, instance=size)
        if form.is_valid():
            form.save()
            return redirect('adminpanel:size_list')
    else:
        form = SizeForm(instance=size)
    return render(request, 'adminpanel/size_form.html', {'form': form, 'size': size})

@login_required
@user_passes_test(admin_required)
def size_delete(request, size_id):
    size = get_object_or_404(Size, id=size_id)
    size.delete()
    return redirect('adminpanel:size_list')
