"""LangGraph Advisory Workflow for Rural Micro-Entrepreneurs.

Coordinates multi-node analysis:
- Node 1: Financial Analysis (calculates profit, break-even, EMI, margins)
- Node 2: Local Market Research (rural demand patterns, competition, working capital)
- Node 3: Scheme & Financing (matching verified government schemes & subsidies)
- Node 4: Advisory Generation (synthesizes findings, risks, mitigations, and recommendations)
"""

from typing import Any, NotRequired, TypedDict
from langgraph.graph import StateGraph, START, END

from finance.calculators import (
    calculate_monthly_profit,
    calculate_break_even_sales,
    calculate_loan_emi,
    calculate_profit_margin,
    calculate_emi_to_revenue_ratio,
)
from .gemini_service import (
    fetch_market_intel_from_gemini,
    fetch_schemes_from_gemini,
    generate_ai_advisory_from_gemini,
)
from .market_data import evaluate_market_dynamics


class AdvisoryState(TypedDict):
    # Core Financial Inputs
    monthly_revenue: float
    monthly_fixed_costs: float
    variable_cost_ratio: float
    loan_amount: float
    annual_interest_rate: float
    loan_tenure_months: int

    # Business Profile & Local Context Inputs (optional with defaults)
    business_name: NotRequired[str]
    business_type: NotRequired[str]
    village: NotRequired[str]
    district: NotRequired[str]
    state: NotRequired[str]
    available_capital: NotRequired[float]
    user_goals: NotRequired[str]

    # Node Output States
    financial_analysis: NotRequired[dict[str, Any]]
    market_research: NotRequired[dict[str, Any]]
    government_schemes: NotRequired[list[dict[str, Any]]]
    recommendations: NotRequired[list[str]]
    risks_and_mitigations: NotRequired[list[dict[str, str]]]
    assumptions_and_sources: NotRequired[dict[str, Any]]
    advisory_summary: NotRequired[str]


# ---------------------------------------------------------------------------
# Node 1: Financial Analysis
# ---------------------------------------------------------------------------
def analyze_finances(state: AdvisoryState) -> dict[str, Any]:
    revenue = float(state.get("monthly_revenue", 0))
    fixed_costs = float(state.get("monthly_fixed_costs", 0))
    variable_ratio = float(state.get("variable_cost_ratio", 0))

    variable_costs = revenue * variable_ratio
    total_expenses = fixed_costs + variable_costs

    profit = calculate_monthly_profit(revenue, total_expenses)
    break_even = calculate_break_even_sales(fixed_costs, variable_ratio)
    margin = calculate_profit_margin(revenue, profit)

    loan_amount = float(state.get("loan_amount", 0))
    annual_rate = float(state.get("annual_interest_rate", 0))
    tenure_months = int(state.get("loan_tenure_months", 12))

    emi = None
    emi_ratio = None

    if loan_amount > 0:
        emi = calculate_loan_emi(loan_amount, annual_rate, tenure_months)
        if revenue > 0:
            emi_ratio = calculate_emi_to_revenue_ratio(emi, revenue)

    # Debt service health evaluation
    repayment_health = "No debt"
    if emi_ratio is not None:
        if emi_ratio <= 15:
            repayment_health = "Safe (EMI is under 15% of revenue)"
        elif emi_ratio <= 25:
            repayment_health = "Moderate (EMI is between 15% and 25% of revenue)"
        else:
            repayment_health = "High Risk (EMI exceeds 25% of revenue)"

    return {
        "financial_analysis": {
            "monthly_revenue": revenue,
            "monthly_fixed_costs": fixed_costs,
            "variable_costs": round(float(variable_costs), 2),
            "total_monthly_expenses": round(float(total_expenses), 2),
            "monthly_profit": round(float(profit), 2),
            "break_even_sales": round(float(break_even), 2),
            "profit_margin_percent": round(float(margin), 2) if margin is not None else None,
            "estimated_monthly_emi": round(float(emi), 2) if emi is not None else None,
            "emi_to_revenue_ratio": round(float(emi_ratio), 2) if emi_ratio is not None else None,
            "repayment_health": repayment_health,
        }
    }


# ---------------------------------------------------------------------------
# Node 2: Local Market Research (Powered by Gemini AI)
# ---------------------------------------------------------------------------
def analyze_market(state: AdvisoryState) -> dict[str, Any]:
    b_type = state.get("business_type", "other")
    b_name = state.get("business_name", "")
    village = state.get("village", "")
    district = state.get("district", "")
    st = state.get("state", "Jharkhand")
    monthly_rev = float(state.get("monthly_revenue", 0))
    capital = float(state.get("available_capital", 0))

    market_insights = fetch_market_intel_from_gemini(
        business_type=b_type,
        business_name=b_name,
        village=village,
        district=district,
        state=st,
        monthly_revenue=monthly_rev,
        available_capital=capital,
    )

    return {"market_research": market_insights}


# ---------------------------------------------------------------------------
# Node 3: Scheme & Financing (Powered by Gemini AI)
# ---------------------------------------------------------------------------
def identify_schemes(state: AdvisoryState) -> dict[str, Any]:
    b_type = state.get("business_type", "other")
    b_name = state.get("business_name", "")
    village = state.get("village", "")
    district = state.get("district", "")
    st = state.get("state", "Jharkhand")
    loan_amt = float(state.get("loan_amount", 0))
    capital = float(state.get("available_capital", 0))
    monthly_rev = float(state.get("monthly_revenue", 0))

    schemes = fetch_schemes_from_gemini(
        business_type=b_type,
        business_name=b_name,
        village=village,
        district=district,
        state=st,
        loan_amount=loan_amt,
        available_capital=capital,
        monthly_revenue=monthly_rev,
    )

    return {"government_schemes": schemes}


# ---------------------------------------------------------------------------
# Node 4: Advisory Generation & Synthesis (Powered by Gemini AI)
# ---------------------------------------------------------------------------
def generate_advisory(state: AdvisoryState) -> dict[str, Any]:
    fin = state.get("financial_analysis", {})
    mkt = state.get("market_research", {})
    schemes = state.get("government_schemes", [])

    b_name = state.get("business_name") or "Your Enterprise"
    b_type = state.get("business_type", "business")
    village = state.get("village", "")
    district = state.get("district", "")
    st = state.get("state", "")
    location_str = f"{village}, {district}, {st}".strip(", ") or "Rural Region"

    # 1. Try Gemini AI synthesis fusing Python financial numbers + Market intel + Schemes
    ai_advisory = generate_ai_advisory_from_gemini(
        business_name=b_name,
        business_type=b_type,
        location_str=location_str,
        financial_analysis=fin,
        market_research=mkt,
        government_schemes=schemes,
    )

    if ai_advisory and ai_advisory.get("advisory_summary"):
        assumptions_and_sources = {
            "cost_model": "Linear break-even analysis: Break-Even = Fixed Costs / (1 - Variable Cost Ratio).",
            "emi_calculation": "Standard reducing-balance amortization formula.",
            "scheme_sources": "KVIC PMEGP, MUDRA Portal, PMMSY Fisheries, State Livelihood Missions.",
            "advisory_engine": "Synthesized with Google Gemini AI grounded in Python financial metrics.",
        }
        return {
            "advisory_summary": ai_advisory["advisory_summary"],
            "recommendations": ai_advisory["recommendations"],
            "risks_and_mitigations": ai_advisory["risks_and_mitigations"],
            "assumptions_and_sources": assumptions_and_sources,
        }

    # 2. Resilient Fallback Logic (used when AI is offline or rate-limited)
    revenue = fin.get("monthly_revenue", 0)
    profit = fin.get("monthly_profit", 0)
    break_even = fin.get("break_even_sales", 0)
    margin = fin.get("profit_margin_percent")
    emi = fin.get("estimated_monthly_emi")
    emi_ratio = fin.get("emi_to_revenue_ratio")

    summary_parts = []
    if profit < 0:
        summary_parts.append(
            f"Current projections indicate an operating deficit of ₹{abs(profit):,.2f}/month. "
            f"Monthly expenses (₹{fin.get('total_monthly_expenses', 0):,.2f}) exceed revenue. "
            "A review of pricing structure and reduction of fixed overheads is essential."
        )
    elif revenue < break_even:
        summary_parts.append(
            f"Expected revenue of ₹{revenue:,.2f} is below the estimated break-even target of ₹{break_even:,.2f}. "
            "You need to increase sales volume or improve contribution margins to achieve operational profitability."
        )
    else:
        margin_str = f" with a healthy profit margin of {margin:.1f}%" if margin else ""
        summary_parts.append(
            f"The business indicates viable unit economics{margin_str}, generating ₹{profit:,.2f}/month in estimated profit. "
            f"Projected revenue exceeds the break-even threshold (₹{break_even:,.2f})."
        )

    if emi:
        if emi_ratio and emi_ratio > 25:
            summary_parts.append(
                f"Caution: The loan EMI of ₹{emi:,.2f} accounts for {emi_ratio:.1f}% of monthly revenue, "
                "which places high strain on daily cash flows. Explore government interest subsidies or extend tenure."
            )
        else:
            summary_parts.append(
                f"Debt servicing appears manageable with monthly EMI at ₹{emi:,.2f}."
            )

    advisory_summary = " ".join(summary_parts)

    recommendations: list[str] = []
    if profit <= 0:
        recommendations.append("Cost Optimization: Re-negotiate supplier costs or lower fixed monthly expenses.")
    else:
        recommendations.append(f"Margin Preservation: Maintain pricing discipline to sustain the {margin or 15:.1f}% profit margin.")

    growth_opp = mkt.get("growth_opportunity")
    if growth_opp:
        recommendations.append(f"Market Strategy: {growth_opp}")

    top_scheme = next((s for s in schemes if s.get("is_recommended")), None)
    if top_scheme:
        recommendations.append(f"Financing Scheme: Prioritize applying for {top_scheme['name']}. {top_scheme['match_reason']}")
    else:
        recommendations.append("Financing: Utilize MUDRA Shishu/Kishore loans before opting for high-interest informal borrowing.")

    recommendations.append("Working Capital Buffer: Maintain strict limits on customer credit (udhar) and reserve at least 30 days of operating expenses.")

    risks_and_mitigations: list[dict[str, str]] = []
    for risk in mkt.get("operational_risks", []):
        risks_and_mitigations.append({
            "risk": risk,
            "mitigation": "Establish daily cash reconciliation, maintain emergency backup inventory, and build local customer trust.",
        })

    assumptions_and_sources = {
        "cost_model": "Linear break-even analysis: Break-Even = Fixed Costs / (1 - Variable Cost Ratio).",
        "emi_calculation": "Standard reducing-balance amortization formula.",
        "scheme_sources": "KVIC PMEGP Guidelines, MUDRA Portal, State Livelihood Missions.",
        "market_heuristics": f"Local rural market intelligence tailored for {b_type.capitalize()}.",
    }

    return {
        "advisory_summary": advisory_summary,
        "recommendations": recommendations,
        "risks_and_mitigations": risks_and_mitigations,
        "assumptions_and_sources": assumptions_and_sources,
    }


# ---------------------------------------------------------------------------
# StateGraph Compilation
# ---------------------------------------------------------------------------
builder = StateGraph(AdvisoryState)

builder.add_node("analyze_finances", analyze_finances)
builder.add_node("analyze_market", analyze_market)
builder.add_node("identify_schemes", identify_schemes)
builder.add_node("generate_advisory", generate_advisory)

builder.add_edge(START, "analyze_finances")
builder.add_edge("analyze_finances", "analyze_market")
builder.add_edge("analyze_market", "identify_schemes")
builder.add_edge("identify_schemes", "generate_advisory")
builder.add_edge("generate_advisory", END)

advisory_graph = builder.compile()
