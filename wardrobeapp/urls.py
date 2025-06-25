from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.shop, name='shop'),
    path('shop/mens/', views.mens_clothing, name='mens_clothing'),
    path('shop/womens/', views.womens_clothing, name='womens_clothing'),
]
