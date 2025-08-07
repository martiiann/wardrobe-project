import uuid
from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from products.models import Product, Size


class Order(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Card'),
        ('paypal', 'PayPal'),
    ]

    TRACKING_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
    ]

    DELIVERY_THRESHOLD = Decimal('50.00')
    DELIVERY_FEE = Decimal('5.00')

    # User can be null for guest checkout
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    guest_token = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        null=True,
        blank=True
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    payment_method = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='card',
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    tracking_number = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=20,
        choices=TRACKING_STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"

    def get_guest_order_url(self):
        from django.urls import reverse
        return reverse(
            'orders:guest_order_detail',
            args=[self.id, self.guest_token]
        )

    def get_delivery_fee(self):
        """Calculate delivery fee based on order total."""
        if self.total_price >= self.DELIVERY_THRESHOLD:
            return Decimal('0.00')
        return self.DELIVERY_FEE

    def get_total_with_delivery(self):
        """Total including delivery."""
        return self.total_price + self.get_delivery_fee()


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(
        Size,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        size_display = f" (Size: {self.size.name})" if self.size else ""
        return f"{self.quantity} x {self.product.name}{size_display}"
