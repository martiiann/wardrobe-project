from django.shortcuts import render, get_object_or_404, redirect
from products.models import Product, Size, Category
from .forms import ProductForm, SizeForm
from orders.models import Order
from .forms import OrderUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import cloudinary
from cloudinary.uploader import upload as cloudinary_upload
from cloudinary.exceptions import Error as CloudinaryError

# ✅ Unified admin check
def admin_required(user):
    return user.is_staff or user.is_superuser

@login_required
@user_passes_test(admin_required)
def dashboard(request):
    return redirect('adminpanel:admin_order_list')

@login_required
@user_passes_test(admin_required)
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'adminpanel/category_list.html', {'categories': categories}) 

@login_required
@user_passes_test(admin_required)
def admin_add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        gender = request.POST.get('gender')

        if not name or not slug:
            messages.error(request, "Name and slug are required.")
        elif Category.objects.filter(slug=slug).exists():
            messages.error(request, f"A category with slug '{slug}' already exists.")
        else:
            Category.objects.create(name=name, slug=slug, gender=gender)
            messages.success(request, f"Category '{name}' added successfully.")
            return redirect('adminpanel:admin_category_list')

    return render(request, 'adminpanel/add_category.html')     

@login_required
@user_passes_test(admin_required)
def admin_delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order.delete()
    messages.success(request, f"Order #{order_id} has been deleted successfully.")
    return redirect('adminpanel:admin_order_list')

@login_required
@user_passes_test(admin_required)
def admin_bulk_delete_orders(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids')
        if order_ids:
            Order.objects.filter(id__in=order_ids).delete()
            messages.success(request, f"Deleted {len(order_ids)} order(s) successfully.")
        else:
            messages.warning(request, "No orders selected.")
    return redirect('adminpanel:admin_order_list')


@login_required
@user_passes_test(admin_required)
def admin_delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    messages.success(request, f"Category '{category.name}' deleted successfully.")
    return redirect('adminpanel:admin_category_list')

@login_required
@user_passes_test(admin_required)
def admin_edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        gender = request.POST.get('gender')

        if not name or not slug:
            messages.error(request, "Name and slug are required.")
        else:
            category.name = name
            category.slug = slug
            category.gender = gender
            category.save()
            messages.success(request, f"Category '{name}' updated successfully.")
            return redirect('adminpanel:admin_category_list')

    return render(request, 'adminpanel/edit_category.html', {'category': category})
   
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
    order_items = order.items.all()

    if request.method == 'POST' and form.is_valid():
        form.save()
        order.refresh_from_db()  # Ensure updated values are loaded

        # ✅ Customer order detail URL
        order_detail_url = request.build_absolute_uri(
            reverse('orders:order_detail', args=[order.id])
        )

        # ✅ Always send email if Shipped or Delivered (for testing)
        if order.status in ['Shipped', 'Delivered']:
            print(f"DEBUG: Sending {order.status} email to {order.user.email}")
            subject = f"Your Order #{order.id} Has Been {order.status}"
            message = (
                f"Hi {order.user.username},\n\n"
                f"Your order #{order.id} has been marked as {order.status}.\n"
                f"Tracking Number: {order.tracking_number or 'Not available'}\n\n"
                f"You can view your order here: {order_detail_url}\n\n"
                f"Thank you for shopping with us!"
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [order.user.email])
                messages.success(request, f"Email sent to {order.user.email}")
            except Exception as e:
                print("ERROR:", e)
                messages.error(request, f"Failed to send email: {e}")
        else:
            print("DEBUG: No email sent (status not shipped or delivered)")

        messages.success(request, 'Order updated successfully!')
        return redirect('adminpanel:admin_order_detail', order_id=order.id)

    return render(request, 'adminpanel/order_detail.html', {
        'order': order,
        'form': form,
        'order_items': order_items,
    })


@login_required
@user_passes_test(admin_required)
def product_list(request):
    products = Product.objects.all()
    return render(request, 'adminpanel/product_list.html', {'products': products})

@login_required
@user_passes_test(admin_required)
def product_edit(request, product_id=None):
    from products.models import ProductImage  

    # ✅ Ensure Cloudinary config
    cloudinary.config( 
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET']
    )

    if product_id:
        product = get_object_or_404(Product, id=product_id)
    else:
        product = None

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()

            # ✅ Handle multiple images
            for img in request.FILES.getlist('extra_images'):
                try:
                    # Try uploading to Cloudinary
                    uploaded_image = cloudinary_upload(img)
                    ProductImage.objects.create(
                        product=product,
                        image=uploaded_image['secure_url']
                    )
                except CloudinaryError as e:
                    messages.error(request, f"Image upload failed: {str(e)}")

            messages.success(request, 'Product saved successfully!')
            return redirect('adminpanel:product_list')
        else:
            messages.error(request, "Please correct the errors in the form.")
    else:
        form = ProductForm(instance=product)

    extra_images = product.images.all() if product else []

    return render(request, 'adminpanel/product_form.html', {
        'form': form,
        'product': product,
        'extra_images': extra_images
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

@login_required
@user_passes_test(admin_required)
def delete_product_image(request, image_id):
    from products.models import ProductImage
    image = get_object_or_404(ProductImage, id=image_id)
    product_id = image.product.id
    image.delete()
    messages.success(request, "Product image deleted successfully.")
    return redirect('adminpanel:product_edit', product_id=product_id)
