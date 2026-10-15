from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from advisory.services import analyze_financial_plan
from businesses.models import BusinessProfile
from .calculators import (
    calculate_break_even_sales,
    calculate_emi_to_revenue_ratio,
    calculate_loan_emi,
    calculate_monthly_profit,
    calculate_profit_margin,
)
from .forms import FinancialPlanForm
from .models import FinancialPlan


@login_required
def create_financial_plan(request, business_id):
    business = get_object_or_404(
        BusinessProfile,
        pk=business_id,
        owner=request.user,
    )

    if request.method == "POST":
        form = FinancialPlanForm(request.POST)

        if form.is_valid():
            plan = form.save(commit=False)
            plan.business = business
            plan.save()

            # Execute LangGraph AI Advisory workflow and persist the report
            analyze_financial_plan(plan, force_refresh=True)

            return redirect("financial_plan_detail", plan_id=plan.id)
    else:
        form = FinancialPlanForm()

    return render(
        request,
        "finance/financial_plan_form.html",
        {"form": form, "business": business},
    )


@login_required
def financial_plan_detail(request, plan_id):
    plan = get_object_or_404(
        FinancialPlan.objects.select_related("business"),
        pk=plan_id,
        business__owner=request.user,
    )

    # Optional refresh support
    force_refresh = request.GET.get("refresh") == "1"
    report = analyze_financial_plan(plan, force_refresh=force_refresh)

    profit = calculate_monthly_profit(
        plan.monthly_revenue,
        plan.monthly_fixed_costs
        + plan.monthly_revenue * plan.variable_cost_ratio,
    )

    break_even = calculate_break_even_sales(
        plan.monthly_fixed_costs,
        plan.variable_cost_ratio,
    )

    profit_margin = calculate_profit_margin(
        plan.monthly_revenue,
        profit,
    )

    emi = None
    if plan.loan_amount > 0:
        emi = calculate_loan_emi(
            plan.loan_amount,
            plan.annual_interest_rate,
            plan.loan_tenure_months,
        )

    emi_ratio = None
    if emi is not None and plan.monthly_revenue > 0:
        emi_ratio = calculate_emi_to_revenue_ratio(emi, plan.monthly_revenue)

    return render(
        request,
        "finance/financial_report.html",
        {
            "business": plan.business,
            "plan": plan,
            "report": report,
            "profit": profit,
            "break_even": break_even,
            "emi": emi,
            "profit_margin": profit_margin,
            "emi_ratio": emi_ratio,
            # Backward-compatible context dict for any legacy template accesses
            "advisory_result": {
                "financial_analysis": report.financial_analysis,
                "advisory_summary": report.advisory_summary,
            },
        },
    )
