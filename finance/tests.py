from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from businesses.models import BusinessProfile
from .calculators import (
    calculate_break_even_sales,
    calculate_emi_to_revenue_ratio,
    calculate_loan_emi,
    calculate_monthly_profit,
    calculate_profit_margin,
)
from .models import FinancialPlan


class FinancialCalculatorTests(SimpleTestCase):

    def test_monthly_profit(self):
        result = calculate_monthly_profit(80000, 55000)
        self.assertEqual(result, Decimal("25000"))

    def test_break_even_sales(self):
        result = calculate_break_even_sales(20000, 0.60)
        self.assertEqual(result, Decimal("5E+4"))

    def test_zero_interest_loan(self):
        result = calculate_loan_emi(120000, 0, 12)
        self.assertEqual(result, Decimal("10000"))

    def test_negative_loan_is_rejected(self):
        with self.assertRaises(ValueError):
            calculate_loan_emi(-1000, 10, 12)

    def test_profit_margin(self):
        margin = calculate_profit_margin(100000, 20000)
        self.assertEqual(margin, Decimal("20.00000000000000000000000000"))

    def test_emi_to_revenue_ratio(self):
        ratio = calculate_emi_to_revenue_ratio(5000, 50000)
        self.assertEqual(ratio, Decimal("10.00000000000000000000000000"))


class FinancialPlanViewsTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.client.login(username="testuser", password="password123")
        self.business = BusinessProfile.objects.create(
            owner=self.user,
            business_name="Rural Tailoring Unit",
            business_type="tailoring",
            village="Morinda",
            district="Rupnagar",
            state="Punjab",
            available_capital=Decimal("25000.00"),
        )

    def test_create_financial_plan_post_and_redirect(self):
        url = reverse("create_financial_plan", kwargs={"business_id": self.business.id})
        response = self.client.post(url, {
            "monthly_revenue": "40000",
            "monthly_fixed_costs": "10000",
            "variable_cost_ratio": "0.45",
            "loan_amount": "50000",
            "annual_interest_rate": "8.5",
            "loan_tenure_months": "24",
        })

        # Should redirect to financial_plan_detail
        self.assertEqual(response.status_code, 302)
        plan = FinancialPlan.objects.filter(business=self.business).first()
        self.assertIsNotNone(plan)
        self.assertRedirects(response, reverse("financial_plan_detail", kwargs={"plan_id": plan.id}))

    def test_financial_plan_detail_renders_report(self):
        plan = FinancialPlan.objects.create(
            business=self.business,
            monthly_revenue=Decimal("40000"),
            monthly_fixed_costs=Decimal("10000"),
            variable_cost_ratio=Decimal("0.45"),
            loan_amount=Decimal("50000"),
            annual_interest_rate=Decimal("8.5"),
            loan_tenure_months=24,
        )
        url = reverse("financial_plan_detail", kwargs={"plan_id": plan.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIn("report", response.context)
        self.assertIn("advisory_result", response.context)
        self.assertContains(response, "Rural Tailoring Unit")
