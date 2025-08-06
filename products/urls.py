from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_view, name='shop'),
    path('shop/<str:gender>/<str:category>/', views.product_list_by_gender, name='product_list_by_category'),
    path('shop/<str:gender>/', views.product_list_by_gender, name='product_list_by_gender'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('shop/', views.product_list, name='product_list'),  # optional fallback
]
