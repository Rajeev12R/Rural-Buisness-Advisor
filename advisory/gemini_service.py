"""Gemini AI Service for querying hyper-local market intelligence, government schemes,
and personalized financial advisory for rural micro-entrepreneurs.

Uses Google Gemini (gemini-3.1-flash-lite) for low-latency, token-efficient,
and deeply contextual advice.
"""

import json
import logging
import os
import requests
from typing import Any
from django.conf import settings

from .market_data import evaluate_market_dynamics
from .schemes_data import match_government_schemes

logger = logging.getLogger(__name__)


def _call_gemini_json(prompt: str, max_tokens: int = 1500) -> dict[str, Any] | None:
    """Helper to query the Gemini API with structured JSON output."""
    api_key = getattr(settings, "GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    model_name = getattr(settings, "GEMINI_MODEL", "gemini-3.1-flash-lite") or os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")

    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.3,
            "maxOutputTokens": max_tokens,
            "responseMimeType": "application/json",
        },
    }

    try:
        response = requests.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=14,
        )

        if response.status_code == 200:
            data = response.json()
            candidates = data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                text_content = "".join(p.get("text", "") for p in parts if "text" in p).strip()
                if text_content.startswith("```"):
                    text_content = text_content.strip("`")
                    if text_content.lower().startswith("json"):
                        text_content = text_content[4:].strip()
                return json.loads(text_content)
        else:
            logger.error("Gemini API error (%s): %s", response.status_code, response.text)
    except Exception as e:
        logger.exception("Failed to query Gemini API: %s", e)

    return None


# ---------------------------------------------------------------------------
# Node 2: Local Market Feasibility via Gemini AI
# ---------------------------------------------------------------------------
def fetch_market_intel_from_gemini(
    business_type: str,
    business_name: str = "",
    village: str = "",
    district: str = "",
    state: str = "Jharkhand",
    monthly_revenue: float = 0,
    available_capital: float = 0,
) -> dict[str, Any]:
    """Generates hyper-local rural market intelligence using Gemini AI."""
    location_str = f"{village}, {district}, {state}".strip(", ")

    prompt = f"""You are a rural market research specialist in India.
Analyze the local market dynamics for this specific micro-enterprise:

- Enterprise Name: {business_name or 'Rural Micro-Enterprise'}
- Sector / Activity: {business_type} (Analyze the actual trade described by the name and sector, e.g. fisheries, dairy, kirana, tailoring, etc.)
- Exact Location: Village: {village or 'Rural area'}, District: {district or 'District'}, State: {state or 'India'}
- Initial Capital: INR {available_capital:,.2f}
- Estimated Monthly Revenue: INR {monthly_revenue:,.2f}

Provide concrete, realistic rural market insights specific to this location and trade (e.g. demand for specific goods, local haats/mandis, seasonal issues).
Format strictly as JSON:
{{
  "demand_profile": "Concise realistic local demand summary for this trade in this region",
  "market_channels": [
    "Specific local channel 1 (e.g. village consumers, local bazaar, nearby town mandi)",
    "Specific local channel 2",
    "Specific local channel 3"
  ],
  "competition_level": "Assessment of local competition and customer retention",
  "capital_assessment": "Assessment of whether INR {available_capital:,.2f} capital is adequate for working expenses and stock",
  "operational_risks": [
    "Key operational/environmental risk 1 specific to this trade in this region",
    "Key operational/environmental risk 2"
  ],
  "growth_opportunity": "One high-potential practical technique or value-add to increase earnings"
}}
Do NOT output markdown backticks or text outside the JSON object.
"""

    parsed = _call_gemini_json(prompt, max_tokens=1200)
    if parsed and isinstance(parsed, dict) and "demand_profile" in parsed:
        sector_label = {
            "dairy": "Dairy Farming & Milk Production",
            "grocery": "Village Kirana & General Store",
            "agriculture": "Agriculture & Allied Agri-Services",
            "tailoring": "Tailoring & Garment Making",
            "handicraft": "Rural Handicrafts & Artisanal Goods",
        }.get(business_type.lower(), business_name or business_type.capitalize())

        return {
            "sector_label": sector_label,
            "location": location_str,
            "demand_profile": parsed.get("demand_profile", ""),
            "market_channels": parsed.get("market_channels", []),
            "competition_level": parsed.get("competition_level", "Moderate"),
            "capital_assessment": parsed.get("capital_assessment", "Adequate liquidity reserve."),
            "operational_risks": parsed.get("operational_risks", []),
            "growth_opportunity": parsed.get("growth_opportunity", ""),
        }

    # Safe fallback to local heuristics
    logger.info("Using local market intelligence fallback.")
    return evaluate_market_dynamics(
        business_type=business_type,
        village=village,
        district=district,
        state=state,
        monthly_revenue=monthly_revenue,
        available_capital=available_capital,
    )


# ---------------------------------------------------------------------------
# Node 3: Government Schemes via Gemini AI
# ---------------------------------------------------------------------------
def fetch_schemes_from_gemini(
    business_type: str,
    business_name: str = "",
    village: str = "",
    district: str = "",
    state: str = "Jharkhand",
    loan_amount: float = 0,
    available_capital: float = 0,
    monthly_revenue: float = 0,
) -> list[dict[str, Any]]:
    """Calls Gemini API to dynamically retrieve Central and State government schemes."""
    prompt = f"""You are an expert advisor on Indian Government micro-enterprise schemes and rural financing.
Identify the top 3 most relevant Central and State Government schemes for this rural micro-entrepreneur:

- Enterprise Name: {business_name or 'Micro-Enterprise'}
- Sector / Activity: {business_type} (Take special note of the trade indicated by the name, e.g., fisheries, dairy, food processing, kirana, crafts)
- Location: Village: {village or 'Rural area'}, District: {district or 'District'}, State: {state or 'India'}
- Initial Available Capital: INR {available_capital:,.2f}
- Loan Required: INR {loan_amount:,.2f}
- Projected Monthly Revenue: INR {monthly_revenue:,.2f}

Provide verified schemes (e.g. PMMSY for fisheries, PMEGP, MUDRA Shishu/Kishore, KCC, JSLPS in Jharkhand, PMFME, etc.).
Format strictly as JSON with root array "schemes":
{{
  "schemes": [
    {{
      "id": "short_id",
      "name": "Full Official Scheme Name",
      "ministry": "Implementing Agency / Ministry",
      "is_recommended": true,
      "match_reason": "Specific concise reason why it fits this entrepreneur",
      "subsidy_details": "Exact rural subsidy % or interest concession",
      "loan_type": "Term loan / working capital",
      "key_eligibility": ["Criteria 1", "Criteria 2"],
      "required_documents": ["Aadhaar", "PAN", "Document 3"],
      "application_process": "Concise step-by-step application guidance",
      "official_portal": "https://..."
    }}
  ]
}}
Do NOT output markdown backticks or text outside the JSON object.
"""

    parsed = _call_gemini_json(prompt, max_tokens=1800)
    if parsed and isinstance(parsed, dict):
        schemes_list = parsed.get("schemes", [])
        if isinstance(schemes_list, list) and len(schemes_list) > 0:
            return schemes_list

    # Safe fallback
    logger.info("Using local verified schemes registry fallback.")
    return match_government_schemes(business_type, loan_amount, available_capital, state)


# ---------------------------------------------------------------------------
# Node 4: Advisory Synthesis via Gemini AI
# ---------------------------------------------------------------------------
def generate_ai_advisory_from_gemini(
    business_name: str,
    business_type: str,
    location_str: str,
    financial_analysis: dict[str, Any],
    market_research: dict[str, Any],
    government_schemes: list[dict[str, Any]],
) -> dict[str, Any] | None:
    """Fuses exact financial metrics with market context and schemes into deep, personalized advisory."""
    rev = financial_analysis.get("monthly_revenue", 0)
    profit = financial_analysis.get("monthly_profit", 0)
    break_even = financial_analysis.get("break_even_sales", 0)
    margin = financial_analysis.get("profit_margin_percent", 0)
    emi = financial_analysis.get("estimated_monthly_emi")
    emi_ratio = financial_analysis.get("emi_to_revenue_ratio")
    debt_health = financial_analysis.get("repayment_health", "Safe")

    scheme_names = [s.get("name", "") for s in government_schemes[:3]]

    prompt = f"""You are a seasoned rural business consultant in India.
Synthesize a professional, highly personalized advisory report for this micro-entrepreneur.

ENTERPRISE PROFILE:
- Business: {business_name} ({business_type})
- Location: {location_str}

EXACT DETERMINISTIC FINANCIAL CALCULATIONS (Do NOT change these figures):
- Expected Monthly Revenue: INR {rev:,.2f}
- Monthly Net Profit: INR {profit:,.2f}
- Break-Even Sales Threshold: INR {break_even:,.2f}
- Net Profit Margin: {margin}%
- Estimated Monthly Loan EMI: {'INR ' + str(emi) if emi else 'None (Self-financed)'}
- Debt Repayment Ratio: {str(emi_ratio) + '%' if emi_ratio else 'N/A'} (Status: {debt_health})

MARKET CONTEXT:
- Demand: {market_research.get('demand_profile', '')}
- Opportunity: {market_research.get('growth_opportunity', '')}
- Relevant Schemes Found: {', '.join(scheme_names)}

TASK:
Write an intelligent, realistic, and practical advisory for this rural entrepreneur.
Link the exact numbers to their trade realities (e.g. cash flow periodicity, input costs, debt safety, local market dynamics).

Format strictly as JSON:
{{
  "advisory_summary": "3-4 sentence comprehensive, professional evaluation linking their specific trade in this village with the financial viability and debt burden.",
  "recommendations": [
    "Actionable Recommendation 1 (Cost/Pricing advice tailored to this trade)",
    "Actionable Recommendation 2 (Market & sales expansion advice for this location)",
    "Actionable Recommendation 3 (Scheme/Financing advice utilizing the top matched scheme)",
    "Actionable Recommendation 4 (Cash flow, working capital, or debt management tip)"
  ],
  "risks_and_mitigations": [
    {{
      "risk": "Concrete operational or cash-flow risk specific to this trade and location",
      "mitigation": "Realistic, actionable step the rural entrepreneur can take to protect themselves"
    }},
    {{
      "risk": "Financial or debt service risk during seasonal or lean periods",
      "mitigation": "Concrete cash-reserve or repayment protection strategy"
    }}
  ]
}}
Do NOT output markdown backticks or text outside the JSON object.
"""

    parsed = _call_gemini_json(prompt, max_tokens=1600)
    if parsed and isinstance(parsed, dict) and "advisory_summary" in parsed:
        return {
            "advisory_summary": parsed.get("advisory_summary", ""),
            "recommendations": parsed.get("recommendations", []),
            "risks_and_mitigations": parsed.get("risks_and_mitigations", []),
        }

    return None
