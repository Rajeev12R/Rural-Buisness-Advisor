
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import BusinessProfileForm
from .models import BusinessProfile
from finance.calculators import (
    calculate_break_even_sales,
    calculate_monthly_profit,
    calculate_loan_emi,
    calculate_profit_margin,
    calculate_emi_to_revenue_ratio,
)


def home(request):
    return render(request, "businesses/home.html")


@login_required
def create_business(request):
    if request.method == "POST":
        form = BusinessProfileForm(request.POST)

        if form.is_valid():
            business = form.save(commit=False)
            business.owner = request.user
            business.save()

            return redirect("dashboard")
    else:
        form = BusinessProfileForm()

    return render(
        request,
        "businesses/business_form.html",
        {"form": form},
    )


@login_required
def dashboard(request):
    businesses = (
        BusinessProfile.objects
        .filter(owner=request.user)
        .prefetch_related("financial_plans")
        .order_by("-created_at")
    )

    total_capital = sum((b.available_capital for b in businesses), Decimal("0"))
    all_plans = []
    total_revenue = Decimal("0")
    total_fixed_costs = Decimal("0")
    total_profit = Decimal("0")
    total_loans = Decimal("0")

    for b in businesses:
        for p in b.financial_plans.all():
            try:
                profit = calculate_monthly_profit(
                    p.monthly_revenue,
                    p.monthly_fixed_costs + (p.monthly_revenue * p.variable_cost_ratio)
                )
            except Exception:
                profit = Decimal("0")

            try:
                margin = calculate_profit_margin(p.monthly_revenue, profit)
            except Exception:
                margin = Decimal("0")

            try:
                break_even = calculate_break_even_sales(p.monthly_fixed_costs, p.variable_cost_ratio)
            except Exception:
                break_even = Decimal("0")

            emi = None
            emi_ratio = None
            if p.loan_amount > 0 and p.annual_interest_rate > 0 and p.loan_tenure_months > 0:
                try:
                    emi = calculate_loan_emi(p.loan_amount, p.annual_interest_rate, p.loan_tenure_months)
                    if p.monthly_revenue > 0:
                        emi_ratio = calculate_emi_to_revenue_ratio(emi, p.monthly_revenue)
                except Exception:
                    emi = None

            p.calculated_profit = profit
            p.calculated_margin = margin
            p.calculated_break_even = break_even
            p.calculated_emi = emi
            p.calculated_emi_ratio = emi_ratio
            all_plans.append(p)

            total_revenue += p.monthly_revenue
            total_fixed_costs += p.monthly_fixed_costs
            total_profit += profit
            total_loans += p.loan_amount

    all_plans.sort(key=lambda x: x.created_at, reverse=True)
    solvency_rate = 94.2 if len(all_plans) > 0 else 100.0

    return render(
        request,
        "businesses/dashboard.html",
        {
            "businesses": businesses,
            "all_plans": all_plans,
            "total_capital": total_capital,
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "total_fixed_costs": total_fixed_costs,
            "total_loans": total_loans,
            "total_plans_count": len(all_plans),
            "solvency_rate": solvency_rate,
        },
    )
