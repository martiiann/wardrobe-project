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

    # ✅ Override login/logout to use custom views (for flash messages)
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.update_profile, name='edit_profile'),
    path('my-orders/', views.order_history, name='my_orders'), 

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

    # Namespaced routes
    path('cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('products/', include(('products.urls', 'products'), namespace='products')),
]
