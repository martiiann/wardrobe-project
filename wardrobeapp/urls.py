from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/men/', views.mens_clothing, name='mens_clothing'),
    path('shop/women/', views.womens_clothing, name='womens_clothing'),
    path('shop/<str:gender>/<slug:category_slug>/', views.products_by_category, name='products_by_category'),
]
