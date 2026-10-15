from django.db import models
from finance.models import FinancialPlan


class AdvisoryReport(models.Model):
    """Stores the generated advisory report linked to a FinancialPlan."""

    financial_plan = models.OneToOneField(
        FinancialPlan,
        on_delete=models.CASCADE,
        related_name="advisory_report",
    )
    advisory_summary = models.TextField()
    financial_analysis = models.JSONField(default=dict)
    market_research = models.JSONField(default=dict)
    government_schemes = models.JSONField(default=list)
    recommendations = models.JSONField(default=list)
    risks_and_mitigations = models.JSONField(default=list)
    assumptions_and_sources = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Advisory Report for {self.financial_plan.business.business_name} (#{self.id})"
