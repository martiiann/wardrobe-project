from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'created_at', 'is_completed']
    list_filter = ['created_at']  # Removed 'is_completed'
    inlines = [OrderItemInline]
    search_fields = ['user__username', 'full_name']

    def is_completed(self, obj):
        return obj.status == 'Delivered'  # or your final status
    is_completed.boolean = True  # Adds checkmark icon in admin
    is_completed.short_description = 'Completed'

