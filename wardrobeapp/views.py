from django.shortcuts import render, get_object_or_404
from .models import Product, Category

def home(request):
    return render(request, 'home.html')

def shop(request):
    return render(request, 'products/shop.html')

def mens_clothing(request):
    categories = Category.objects.all()
    products = Product.objects.filter(gender='Men', is_available=True)
    return render(request, 'products/category_products.html', {
        'gender': 'Men',
        'categories': categories,
        'products': products
    })

def womens_clothing(request):
    categories = Category.objects.all()
    products = Product.objects.filter(gender='Women', is_available=True)
    return render(request, 'products/category_products.html', {
        'gender': 'Women',
        'categories': categories,
        'products': products
    })

def products_by_category(request, gender, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, gender=gender, is_available=True)
    return render(request, 'products/products_by_category.html', {
        'category': category,
        'gender': gender,
        'products': products
    })
