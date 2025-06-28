from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.ModelAdmin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_completed']
    list_filter = ['is_completed', 'created_at']
    inlines = [OrderItemInline]
    search_fields = ['user__username', 'full_name']
