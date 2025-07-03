from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from products.models import Product, Category
from .forms import UserRegisterForm

# Home Page
def home(request):
    return render(request, 'home.html')

# Shop Page
def shop(request):
    categories = Category.objects.all()
    products = Product.objects.filter(is_available=True).order_by('-created_at')
    return render(request, 'products/shop.html', {
        'products': products,
        'categories': categories
    })

# Men's Clothing Page
def mens_clothing(request):
    categories = Category.objects.filter(gender='men')
    selected_category_slug = request.GET.get('category')
    products = Product.objects.filter(gender='men', is_available=True)

    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=selected_category)
    else:
        selected_category = None

    return render(request, 'products/category_products.html', {
        'gender': 'Men',
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
    })

# Women's Clothing Page
def womens_clothing(request):
    categories = Category.objects.filter(gender='women')
    selected_category_slug = request.GET.get('category')
    products = Product.objects.filter(gender='women', is_available=True)

    if selected_category_slug:
        selected_category = get_object_or_404(Category, slug=selected_category_slug)
        products = products.filter(category=selected_category)
    else:
        selected_category = None

    return render(request, 'products/category_products.html', {
        'gender': 'Women',
        'categories': categories,
        'products': products,
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
            return redirect('profile')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'auth/login.html')

# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')

# Profile View (Logged-in Users)
@login_required
def profile(request):
    return render(request, 'auth/profile.html')
