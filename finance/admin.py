from django.contrib import admin
from .models import FinancialPlan


@admin.register(FinancialPlan)
class FinancialPlanAdmin(admin.ModelAdmin):
    list_display = (
        "business",
        "monthly_revenue",
        "monthly_fixed_costs",
        "loan_amount",
        "created_at",
    )