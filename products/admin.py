from django.contrib import admin
from .models import Product, Category, Size

admin.site.register(Product)
admin.site.register(Category)

@admin.register(Size)
class SizeAdmin(admin.ModelAdmin):
    list_display = ['name']