from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import BusinessProfile


class BusinessProfileTests(TestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="farmer1", password="password123")
        self.user2 = User.objects.create_user(username="farmer2", password="password123")
        self.b1 = BusinessProfile.objects.create(
            owner=self.user1,
            business_name="Farmer 1 Dairy",
            business_type="dairy",
            village="Village A",
            district="District A",
            state="Punjab",
            available_capital=Decimal("50000"),
        )
        self.b2 = BusinessProfile.objects.create(
            owner=self.user2,
            business_name="Farmer 2 Kirana",
            business_type="grocery",
            village="Village B",
            district="District B",
            state="Punjab",
            available_capital=Decimal("30000"),
        )

    def test_dashboard_user_isolation(self):
        """Ensure users can only see their own businesses."""
        self.client.login(username="farmer1", password="password123")
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Farmer 1 Dairy")
        self.assertNotContains(response, "Farmer 2 Kirana")

    def test_create_business_view(self):
        self.client.login(username="farmer1", password="password123")
        response = self.client.post(reverse("create_business"), {
            "business_name": "Farmer 1 New Tailoring",
            "business_type": "tailoring",
            "village": "Village A",
            "district": "District A",
            "state": "Punjab",
            "available_capital": "20000",
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("dashboard"))
        self.assertTrue(
            BusinessProfile.objects.filter(
                owner=self.user1, business_name="Farmer 1 New Tailoring"
            ).exists()
        )
