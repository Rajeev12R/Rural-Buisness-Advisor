
from django import forms
from .models import FinancialPlan


class FinancialPlanForm(forms.ModelForm):
    class Meta:
        model = FinancialPlan
        fields = [
            "monthly_revenue",
            "monthly_fixed_costs",
            "variable_cost_ratio",
            "loan_amount",
            "annual_interest_rate",
            "loan_tenure_months",
        ]

    def clean(self):
        cleaned_data = super().clean()

        for field in (
            "monthly_revenue",
            "monthly_fixed_costs",
            "loan_amount",
            "annual_interest_rate",
        ):
            value = cleaned_data.get(field)
            if value is not None and value < 0:
                self.add_error(field, "Cannot be negative.")

        ratio = cleaned_data.get("variable_cost_ratio")
        if ratio is not None and not 0 <= ratio < 1:
            self.add_error(
                "variable_cost_ratio",
                "Enter a ratio from 0 inclusive to less than 1.",
            )

        if cleaned_data.get("loan_tenure_months", 0) <= 0:
            self.add_error(
                "loan_tenure_months",
                "Loan tenure must be greater than zero.",
            )

        return cleaned_data
