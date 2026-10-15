"""Advisory Services layer connecting Django models to the LangGraph AI advisory engine."""

from typing import Any
from .graph import advisory_graph
from .models import AdvisoryReport


def analyze_financial_plan(plan, force_refresh: bool = False) -> AdvisoryReport:
    """Run the complete 4-node LangGraph workflow for a saved FinancialPlan and persist the AdvisoryReport."""
    # Check if a report already exists and refresh is not requested
    if not force_refresh:
        existing_report = AdvisoryReport.objects.filter(financial_plan=plan).first()
        if existing_report:
            return existing_report

    business = plan.business

    # Prepare complete input state for the LangGraph advisory engine
    state_input: dict[str, Any] = {
        "monthly_revenue": float(plan.monthly_revenue),
        "monthly_fixed_costs": float(plan.monthly_fixed_costs),
        "variable_cost_ratio": float(plan.variable_cost_ratio),
        "loan_amount": float(plan.loan_amount),
        "annual_interest_rate": float(plan.annual_interest_rate),
        "loan_tenure_months": int(plan.loan_tenure_months),
        "business_name": business.business_name,
        "business_type": business.business_type,
        "village": business.village,
        "district": business.district,
        "state": business.state,
        "available_capital": float(business.available_capital),
    }

    result = advisory_graph.invoke(state_input)

    # Persist or update the AdvisoryReport in SQLite
    report, _ = AdvisoryReport.objects.update_or_create(
        financial_plan=plan,
        defaults={
            "advisory_summary": result.get("advisory_summary", ""),
            "financial_analysis": result.get("financial_analysis", {}),
            "market_research": result.get("market_research", {}),
            "government_schemes": result.get("government_schemes", []),
            "recommendations": result.get("recommendations", []),
            "risks_and_mitigations": result.get("risks_and_mitigations", []),
            "assumptions_and_sources": result.get("assumptions_and_sources", {}),
        },
    )

    return report
