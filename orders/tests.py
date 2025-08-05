from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class OrderHistoryViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
    
    def test_order_history_requires_login(self):
        # User is not logged in → should redirect to login page
        response = self.client.get(reverse("order_history"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/login", response.url)
    
    def test_order_history_logged_in(self):
        # Log the user in
        self.client.login(username="testuser", password="password123")
        response = self.client.get(reverse("order_history"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "orders/order_history.html")
