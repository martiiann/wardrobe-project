from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/men/', views.mens_clothing, name='mens_clothing'),
    path('shop/women/', views.womens_clothing, name='womens_clothing'),
    path('shop/<str:gender>/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),

    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # ✅ Use namespace for cart
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),

    # ✅ Register the products app with a namespace
    path('products/', include(('products.urls', 'products'), namespace='products')),
]
