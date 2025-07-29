from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),
    path('orders/', views.order_list, name='admin_order_list'),
    path('orders/<int:order_id>/', views.order_detail, name='admin_order_detail'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_edit, name='product_add'),
    path('products/<int:product_id>/edit/', views.product_edit, name='product_edit'),
    path('products/<int:product_id>/delete/', views.product_delete, name='product_delete'),
    path('sizes/', views.size_list, name='size_list'),
    path('sizes/add/', views.size_form, name='size_add'),
    path('sizes/<int:size_id>/edit/', views.size_form, name='size_edit'),
    path('sizes/<int:size_id>/delete/', views.size_delete, name='size_delete'),

    # ✅ New delete product image route
    path('products/images/<int:image_id>/delete/', views.delete_product_image, name='delete_product_image'),
]