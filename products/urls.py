from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),  # /shop/
    path('<str:gender>/<str:category>/', views.product_list_by_gender, name='product_list_by_category'),
    path('<str:gender>/', views.product_list_by_gender, name='product_list_by_gender'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
]
