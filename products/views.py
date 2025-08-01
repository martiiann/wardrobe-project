from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.urls import reverse

def shop_view(request):
    men_categories = Category.objects.filter(gender='men')
    women_categories = Category.objects.filter(gender='women')
    return render(request, 'products/shop.html', {
        'men_categories': men_categories,
        'women_categories': women_categories,
    })

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'products/category_products.html', {
        'category': category,
        'products': products,
    })

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/shop.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    # ✅ Detect if came from cart
    from_cart = request.GET.get('from_cart') == 'true'
    if from_cart:
        request.session['from_cart'] = True
    else:
        request.session.pop('from_cart', None)

    # ✅ Detect if came from order
    from_order = request.GET.get('from_order')
    if from_order:
        request.session['from_order'] = from_order
    else:
        request.session.pop('from_order', None)

    # ✅ Store previous page for Continue Shopping
    referer = request.META.get('HTTP_REFERER')
    if referer and 'product_detail' not in referer:
        request.session['prev_page'] = referer

    return render(request, 'products/product_detail.html', {
        'product': product,
        'from_cart': request.session.get('from_cart', False),
        'from_order': request.session.get('from_order', None),
        'prev_page': request.session.get('prev_page')
    })