from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Product


def shop_view(request):
    men_categories = Category.objects.filter(gender='men')
    women_categories = Category.objects.filter(gender='women')

    return render(request, 'products/shop.html', {
        'men_categories': men_categories,
        'women_categories': women_categories,
    })


def product_list(request):
    products = Product.objects.all()
    search_query = request.GET.get('search', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/shop.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'search_query': search_query
    })


def product_list_by_gender(request, gender):
    gender = gender.lower()
    categories = Category.objects.filter(gender=gender)
    products = Product.objects.filter(gender=gender)

    category_slug = request.GET.get('category')
    selected_category = None
    if category_slug:
        selected_category = get_object_or_404(Category, slug=category_slug, gender=gender)
        products = products.filter(category=selected_category)

    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category_products.html', {
        'products': page_obj,
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': selected_category,
        'category': selected_category if selected_category else {'name': 'All'},
        'search_query': search_query,
        'gender': gender,
    })


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    search_query = request.GET.get('search', '')

    if search_query:
        products = products.filter(name__icontains=search_query)

    paginator = Paginator(products, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/category_products.html', {
        'category': category,
        'products': page_obj,
        'page_obj': page_obj,
        'search_query': search_query,
    })


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    from_cart = request.GET.get('from_cart') == 'true'
    if from_cart:
        request.session['from_cart'] = True
    else:
        request.session.pop('from_cart', None)

    from_order = request.GET.get('from_order')
    if from_order:
        request.session['from_order'] = from_order
    else:
        request.session.pop('from_order', None)

    referer = request.META.get('HTTP_REFERER')
    if referer and 'product_detail' not in referer:
        request.session['prev_page'] = referer

    return render(request, 'products/product_detail.html', {
        'product': product,
        'from_cart': request.session.get('from_cart', False),
        'from_order': request.session.get('from_order', None),
        'prev_page': request.session.get('prev_page')
    })
