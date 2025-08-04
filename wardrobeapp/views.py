from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Category, Size
from .forms import UserRegisterForm, UserUpdateForm  # Make sure you have this form
from cart.cart import Cart
from django.views.decorators.http import require_POST
from orders.models import Order  # Assuming you have an Order model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.db.models import Q
from django.core.paginator import Paginator 

# Home Page
def home(request):
    return render(request, 'home.html')

# Shop Page
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    gender = "All"

    # Add pagination
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'products/shop.html', {
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'categories': categories,
        'gender': gender
    })

@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = Cart(request)

    size_id = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    size = get_object_or_404(Size, id=size_id) if size_id else None

    cart.add(product, size=size, quantity=quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'name': product.name,
            'image': product.image.url if product.image else '',
            'quantity': quantity,
            'price': float(product.price),
            'size': size.name if size else '',
            'cart_count': cart.count(),
            'cart_total_price': float(cart.get_total_price()),
            'cart_total_items': len(cart),
        })

    return redirect('cart:detail')

# Men's Clothing Page
def mens_clothing(request):
    categories = Category.objects.filter(gender='men')
    selected_category_slug = request.GET.get('category')
    search_query = request.GET.get('search')  # 🔍 NEW
    products = Product.objects.filter(gender='men', is_available=True)

    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=selected_category)
    else:
        selected_category = None

    if search_query:  # 🔍 Filter by name or description
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category_products.html', {
        'gender': 'Men',
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
    })


# Women's Clothing Page
def womens_clothing(request):
    categories = Category.objects.filter(gender='women')
    selected_category_slug = request.GET.get('category')
    search_query = request.GET.get('search')  # 🔍 NEW
    products = Product.objects.filter(gender='women', is_available=True)

    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=selected_category)
    else:
        selected_category = None

    if search_query:  # 🔍 Filter by name or description
        products = products.filter(
            Q(name__icontains=search_query) | Q(description__icontains=search_query)
        )

    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category_products.html', {
        'gender': 'Women',
        'categories': categories,
        'products': page_obj.object_list,
        'page_obj': page_obj,
        'selected_category': selected_category,
    })

# Products by Category (Gender + Category)
def products_by_category(request, gender, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, gender=gender, is_available=True)
    return render(request, 'products/products_by_category.html', {
        'category': category,
        'gender': gender,
        'products': products
    })

# Product Detail
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# ---------------------------
# Authentication Views Below
# ---------------------------

# Register New User
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Only login if profile does not already exist
            if not hasattr(user, 'profile'):
                # Signal should handle this, but just in case:
                from wardrobeapp.models import Profile
                Profile.objects.get_or_create(user=user)

            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('profile')
    else:
        form = UserRegisterForm()
    return render(request, 'auth/register.html', {'form': form})

# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, 'Successfully signed in!')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth/login.html')

# Logout View
def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# Profile View (Logged-in Users)
@login_required
def profile(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'auth/profile.html', {
        'orders': orders
    })

# Order History View
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

# Order Detail View
@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

# Update Profile View
@login_required
def update_profile(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfileUpdateForm(instance=request.user.profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('profile')

    return render(request, 'auth/update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

def custom_permission_denied_view(request, exception=None):
    return render(request, '403.html', status=403)