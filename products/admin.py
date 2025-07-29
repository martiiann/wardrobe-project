from django.contrib import admin
from .models import Product, ProductImage, Category, Size

# Inline for extra images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

# Product admin with images inline
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available', 'gender']
    search_fields = ['name', 'description']
    inlines = [ProductImageInline]

# Category admin
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'gender']

# Size admin
@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']

# ProductImage admin (optional direct access)
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'uploaded_at']
