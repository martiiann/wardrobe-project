from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('category/<slug:slug>/', views.category_products, name='category_products'),
]
