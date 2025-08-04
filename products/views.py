from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product


def shop_view(request):
    men_categories = Category.objects.filter(gender='men')
    women_categories = Category.objects.filter(gender='women')

    products = Product.objects.all()
    search_query = request.GET.get('search', '')

    # 🔍 Optional search filter
    if search_query:
        products = products.filter(name__icontains=search_query)

    # 🔄 Pagination
    paginator = Paginator(products, 6)  # Show 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/shop.html', {
        'men_categories': men_categories,
        'women_categories': women_categories,
        'products': page_obj,   # ✅ Pass paginated products
        'page_obj': page_obj,   # ✅ Pass for pagination controls
        'search_query': search_query,
    })

def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')

    # 🔍 Apply search filter
    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/shop.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    search_query = request.GET.get('search', '')

    # 🔍 Apply search filter if any
    if search_query:
        products = products.filter(name__icontains=search_query)

    # 🔄 Pagination (6 per page)
    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category_products.html', {
        'category': category,
        'products': page_obj,  # now paginated
        'page_obj': page_obj,
        'search_query': search_query,
    })

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