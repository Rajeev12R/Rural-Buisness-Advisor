from decimal import Decimal
from django.contrib.auth.models import User
from django.test import TestCase

from businesses.models import BusinessProfile
from finance.models import FinancialPlan
from .graph import advisory_graph
from .models import AdvisoryReport
from .services import analyze_financial_plan


class AdvisoryGraphTests(TestCase):

    def test_graph_calculates_financial_analysis(self):
        """Test backwards compatibility with minimal input state."""
        result = advisory_graph.invoke({
            "monthly_revenue": 80000,
            "monthly_fixed_costs": 20000,
            "variable_cost_ratio": 0.60,
            "loan_amount": 120000,
            "annual_interest_rate": 0,
            "loan_tenure_months": 12,
        })

        analysis = result["financial_analysis"]
        self.assertAlmostEqual(analysis["monthly_profit"], 12000)
        self.assertAlmostEqual(analysis["break_even_sales"], 50000)
        self.assertAlmostEqual(analysis["estimated_monthly_emi"], 10000)
        self.assertTrue(result["advisory_summary"])
        self.assertIn("recommendations", result)
        self.assertIn("market_research", result)
        self.assertIn("government_schemes", result)

    def test_full_advisory_pipeline_dairy(self):
        """Test full 4-node pipeline for a rural dairy micro-business."""
        result = advisory_graph.invoke({
            "business_name": "Kishan Dairy",
            "business_type": "dairy",
            "village": "Rampur",
            "district": "Ludhiana",
            "state": "Punjab",
            "available_capital": 50000,
            "monthly_revenue": 60000,
            "monthly_fixed_costs": 15000,
            "variable_cost_ratio": 0.50,
            "loan_amount": 100000,
            "annual_interest_rate": 7.0,
            "loan_tenure_months": 24,
        })

        # Node 1: Financial Analysis checks
        fin = result["financial_analysis"]
        self.assertEqual(fin["monthly_revenue"], 60000)
        self.assertEqual(fin["monthly_fixed_costs"], 15000)
        self.assertGreater(fin["monthly_profit"], 0)
        self.assertIsNotNone(fin["estimated_monthly_emi"])
        self.assertIsNotNone(fin["emi_to_revenue_ratio"])

        # Node 2: Market Research checks
        mkt = result["market_research"]
        self.assertIn("Dairy", mkt["sector_label"])
        self.assertIn("Ludhiana", mkt["location"])
        self.assertTrue(mkt["market_channels"])
        self.assertTrue(mkt["operational_risks"])

        # Node 3: Scheme & Financing checks
        schemes = result["government_schemes"]
        self.assertGreater(len(schemes), 0)
        scheme_ids = [s["id"].lower() for s in schemes]
        self.assertTrue(any("pmegp" in sid or "mudra" in sid or "kcc" in sid for sid in scheme_ids))

        # Node 4: Advisory Generation checks
        self.assertTrue(len(result["recommendations"]) > 0)
        self.assertTrue(len(result["risks_and_mitigations"]) > 0)
        self.assertIn("cost_model", result["assumptions_and_sources"])
        self.assertIn("viable", result["advisory_summary"].lower())

    def test_analyze_financial_plan_service_persists_report(self):
        """Test service correctly creates and updates AdvisoryReport in DB."""
        user = User.objects.create_user(username="testfarmer", password="password123")
        business = BusinessProfile.objects.create(
            owner=user,
            business_name="Green Harvest Grocery",
            business_type="grocery",
            village="Nabha",
            district="Patiala",
            state="Punjab",
            available_capital=Decimal("40000.00"),
        )
        plan = FinancialPlan.objects.create(
            business=business,
            monthly_revenue=Decimal("50000.00"),
            monthly_fixed_costs=Decimal("12000.00"),
            variable_cost_ratio=Decimal("0.6500"),
            loan_amount=Decimal("50000.00"),
            annual_interest_rate=Decimal("9.50"),
            loan_tenure_months=12,
        )

        report = analyze_financial_plan(plan)

        self.assertIsInstance(report, AdvisoryReport)
        self.assertEqual(report.financial_plan, plan)
        self.assertTrue(report.advisory_summary)
        self.assertIn("monthly_profit", report.financial_analysis)
        self.assertTrue(len(report.government_schemes) > 0)
        self.assertTrue(len(report.recommendations) > 0)

        # Confirm retrieval from SQLite
        db_report = AdvisoryReport.objects.get(financial_plan=plan)
        self.assertEqual(db_report.id, report.id)
