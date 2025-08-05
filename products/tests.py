from django.test import TestCase
from products.models import Category, Product

class ProductModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Men's Clothing")

    def test_product_str(self):
        product = Product.objects.create(
            name="Test Jacket",
            category=self.category,
            description="Test description",
            price=49.99,
            is_available=True,
            gender="M"
        )
        self.assertEqual(str(product), "Test Jacket")
