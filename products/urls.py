from django.urls import path
from . import views

app_name = 'products'  # ✅ Required for namespacing

urlpatterns = [
    path(
        '',
        views.product_list,
        name='product_list',
    ),
    path(
        'product/<int:pk>/',
        views.product_detail,
        name='product_detail',
    ),
    path(
        '<str:gender>/',
        views.product_list_by_gender,
        name='product_list_by_gender',
    ),
    path(
        '<str:gender>/<str:category>/',
        views.product_list_by_gender,
        name='product_list_by_category',
    ),
]
