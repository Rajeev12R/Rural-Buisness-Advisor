
from django.db import models
from django.conf import settings
from businesses.models import BusinessProfile


class FinancialPlan(models.Model):
    business = models.ForeignKey(
        BusinessProfile,
        on_delete=models.CASCADE,
        related_name="financial_plans",
    )

    monthly_revenue = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    monthly_fixed_costs = models.DecimalField(
        max_digits=12, decimal_places=2
    )
    variable_cost_ratio = models.DecimalField(
        max_digits=5, decimal_places=4
    )

    loan_amount = models.DecimalField(
        max_digits=12, decimal_places=2,
        default=0,
    )
    annual_interest_rate = models.DecimalField(
        max_digits=5, decimal_places=2,
        default=0,
    )
    loan_tenure_months = models.PositiveIntegerField(default=12)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Financial plan for {self.business.business_name}"
