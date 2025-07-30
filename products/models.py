from django.db import models
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(
        max_length=10,
        choices=[('men', 'Men'), ('women', 'Women')],
        default='men'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f"{self.name} ({self.gender})"

class Size(models.Model):
    name = models.CharField(max_length=10)  # e.g., 'S', 'M', 'L', 'XL'

    def __str__(self):
        return self.name

class Product(models.Model):
    GENDER_CHOICES = [
        ('men', 'Men'),
        ('women', 'Women'),
    ]

    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    is_available = models.BooleanField(default=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    sizes = models.ManyToManyField(Size, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    def get_current_price(self):
        return self.price

    def get_absolute_url(self):
        return reverse('product_detail', args=[str(self.id)])
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"