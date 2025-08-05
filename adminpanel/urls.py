from django.urls import path
from . import views

app_name = 'adminpanel'

urlpatterns = [
    path('', views.dashboard, name='admin_dashboard'),

    path('orders/', views.order_list, name='admin_order_list'),
    path(
        'orders/<int:order_id>/',
        views.order_detail,
        name='admin_order_detail'
    ),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_edit, name='product_add'),
    path(
        'products/<int:product_id>/edit/',
        views.product_edit,
        name='product_edit'
    ),
    path(
        'products/<int:product_id>/delete/',
        views.product_delete,
        name='product_delete'
    ),

    path('sizes/', views.size_list, name='size_list'),
    path('sizes/add/', views.size_form, name='size_add'),
    path(
        'sizes/<int:size_id>/edit/',
        views.size_form,
        name='size_edit'
    ),
    path(
        'sizes/<int:size_id>/delete/',
        views.size_delete,
        name='size_delete'
    ),

    path(
        'categories/',
        views.admin_category_list,
        name='admin_category_list'
    ),
    path(
        'categories/add/',
        views.admin_add_category,
        name='admin_add_category'
    ),
    path(
        'categories/delete/<int:category_id>/',
        views.admin_delete_category,
        name='admin_delete_category'
    ),
    path(
        'categories/<int:category_id>/edit/',
        views.admin_edit_category,
        name='admin_edit_category'
    ),

    path(
        'orders/<int:order_id>/delete/',
        views.admin_delete_order,
        name='admin_delete_order'
    ),
    path(
        'orders/bulk-delete/',
        views.admin_bulk_delete_orders,
        name='admin_bulk_delete_orders'
    ),

    # ✅ New delete product image route
    path(
        'products/images/<int:image_id>/delete/',
        views.delete_product_image,
        name='delete_product_image'
    ),
]