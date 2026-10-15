"""Rural Market Research and Local Feasibility Knowledge Base.

Provides structured market intelligence, demand patterns, competition dynamics,
and local operating risks for rural micro-enterprises.
"""

from typing import Any

SECTOR_MARKET_INTELLIGENCE: dict[str, dict[str, Any]] = {
    "dairy": {
        "sector_label": "Dairy Farming & Milk Production",
        "demand_profile": "High and steady daily local demand. Milk and dairy products (curd, paneer, ghee) have daily recurring consumption.",
        "market_channels": [
            "Local village households and tea stalls (immediate daily cash realization)",
            "Village Dairy Cooperative Societies (e.g., Amul, Verka, Saras, Nandini, Mother Dairy) with bi-weekly fat/SNF-tested payouts",
            "Nearby semi-urban sweet shops and confectioneries for bulk milk supply",
        ],
        "competition_level": "Moderate. Competition is based on milk quality, fat testing transparency, and consistency of supply.",
        "key_cost_drivers": [
            "Green fodder and dry fodder availability",
            "Cattle feed concentrates (oil cakes, bran)",
            "Veterinary healthcare, artificial insemination, and vaccinations",
        ],
        "operational_risks": [
            "Perishability of raw milk requiring cold chain or timely morning/evening collection",
            "Seasonal dry period of milch animals leading to cyclical revenue dips",
            "Cattle health risks and disease outbreaks requiring prompt immunization",
        ],
        "rural_opportunity": "High potential for value addition: converting surplus milk into curd, paneer, and clarified butter (ghee) yielding 25-40% higher realization.",
    },
    "grocery": {
        "sector_label": "Village Kirana & General Store",
        "demand_profile": "Constant, inelastic demand for daily household essentials, grains, cooking oil, spices, soaps, and packaged foods.",
        "market_channels": [
            "Direct village walk-in retail footfall",
            "Weekly rural market (haat / bazaar) pop-up stalls",
            "School and village junction snack retail",
        ],
        "competition_level": "High in main village squares. Differentiation relies on product availability, fresh inventory, and fair customer relations.",
        "key_cost_drivers": [
            "Inventory replenishment transport costs from district wholesale mandi",
            "Shop rental in central village locations or electricity costs",
            "Customer credit (udhar khata) working capital absorption",
        ],
        "operational_risks": [
            "Uncollected customer credit (udhar) choking liquid working capital",
            "Expiry and rodent damage on packaged commodities",
            "Price fluctuation of bulk commodities (oil, sugar, pulses)",
        ],
        "rural_opportunity": "Adding high-margin complementary services such as digital recharge/AePS micro-ATM cash withdrawals and packaged dairy products.",
    },
    "agriculture": {
        "sector_label": "Agriculture & Allied Agri-Services",
        "demand_profile": "Season-driven strong demand aligned with Kharif, Rabi, and Zaid crop calendars.",
        "market_channels": [
            "APMC Mandis and local agricultural markets",
            "Farmer Producer Organizations (FPOs) and aggregation centers",
            "Direct farm-gate procurement by regional traders",
        ],
        "competition_level": "Moderate. Market price is determined by mandi arrivals and government Minimum Support Price (MSP).",
        "key_cost_drivers": [
            "Certified quality seeds, bio-fertilizers, and crop protection inputs",
            "Irrigation electricity / diesel pump expenses",
            "Tractor tillage, harvesting, and manual labor wages",
        ],
        "operational_risks": [
            "Monsoon irregularity and climate fluctuations",
            "Post-harvest price crash during peak arrival seasons",
            "Storage losses due to lack of local warehousing or solar dryers",
        ],
        "rural_opportunity": "Crop diversification into high-value horticultural crops (vegetables, flowers, medicinal plants) and micro-irrigation drip subsidies.",
    },
    "tailoring": {
        "sector_label": "Tailoring & Garment Making",
        "demand_profile": "Consistent regular stitching demand with pronounced festive, wedding, and school uniform season peaks.",
        "market_channels": [
            "Village women and family custom stitching orders",
            "Local school uniform contracts",
            "Nearby weekly bazaar stalls for readymade blouse/petticoat/kurta sales",
        ],
        "competition_level": "Low to Moderate. Strong customer retention through punctuality, precise fit, and modern design catalog.",
        "key_cost_drivers": [
            "Sewing machine maintenance, needles, threads, buttons, and zippers",
            "Fabric inventory if providing stitched ready-to-wear pieces",
            "Electricity or solar power backup for mechanized machines",
        ],
        "operational_risks": [
            "Seasonal slump in non-wedding/non-festival months",
            "Competition from inexpensive mass-manufactured readymade garments",
            "Single-person labor bottleneck during peak seasons",
        ],
        "rural_opportunity": "Forming Self-Help Group (SHG) clusters to undertake bulk institutional uniform supply and designer boutique tailoring.",
    },
    "handicraft": {
        "sector_label": "Rural Handicrafts & Artisanal Goods",
        "demand_profile": "Niche but high-value demand, expanding rapidly through district exhibitions, cultural tourism, and regional buyers.",
        "market_channels": [
            "District SARAS fairs, Shilpgrams, and state artisan expos",
            "Khadi and Village Industries Commission (KVIC) emporiums",
            "Tribal / Rural cooperative marketing federations (TRIFED / State Handloom)",
        ],
        "competition_level": "Low local competition; competition against synthetic industrial alternatives.",
        "key_cost_drivers": [
            "Authentic raw materials (clay, bamboo, natural dyes, cane, yarn)",
            "Specialized hand tools and traditional casting/weaving equipment",
            "Protective packaging and freight to exhibition / urban buyers",
        ],
        "operational_risks": [
            "Irregular cash flows between batch sales",
            "Middlemen capturing retail margins while paying low artisan procurement rates",
            "Lack of formal GI tag or branding",
        ],
        "rural_opportunity": "Direct-to-consumer onboarding via ONDC (Open Network for Digital Commerce) and SHG federations eliminating middlemen.",
    },
    "other": {
        "sector_label": "Rural Micro-Enterprise",
        "demand_profile": "Targeted local demand responding to specific unmet service or retail gaps in the village or panchayat.",
        "market_channels": ["Direct village consumers and regional market networks"],
        "competition_level": "Moderate depending on village accessibility to neighboring town centers.",
        "key_cost_drivers": ["Input raw materials, utility costs, and local transport"],
        "operational_risks": ["Demand fluctuations and customer credit management"],
        "rural_opportunity": "Leveraging village community trust and customized door-to-door customer service.",
    },
}


def evaluate_market_dynamics(
    business_type: str,
    village: str = "",
    district: str = "",
    state: str = "",
    monthly_revenue: float = 0,
    available_capital: float = 0,
) -> dict[str, Any]:
    """Generates rural market feasibility and competition assessment."""
    b_type = (business_type or "other").lower().strip()
    intel = SECTOR_MARKET_INTELLIGENCE.get(
        b_type, SECTOR_MARKET_INTELLIGENCE["other"]
    )

    location_str = f"{village}, {district}, {state}".strip(", ")
    if not location_str:
        location_str = "Local Rural Cluster"

    # Analyze working capital adequacy
    capital_assessment = "Adequate"
    if available_capital > 0 and monthly_revenue > 0:
        ratio = available_capital / monthly_revenue
        if ratio < 0.5:
            capital_assessment = (
                "Tight capital cushion. Immediate focus should be on prompt cash realization and lean inventory."
            )
        elif ratio < 1.5:
            capital_assessment = (
                "Balanced capital structure covering 1-2 months of operational working capital."
            )
        else:
            capital_assessment = (
                "Comfortable liquidity reserve available to absorb seasonal dips or scale production."
            )
    else:
        capital_assessment = "Ensure at least 1-2 months of fixed operating costs are held in liquid reserves."

    return {
        "sector_label": intel["sector_label"],
        "location": location_str,
        "demand_profile": intel["demand_profile"],
        "market_channels": intel["market_channels"],
        "competition_level": intel["competition_level"],
        "key_cost_drivers": intel["key_cost_drivers"],
        "operational_risks": intel["operational_risks"],
        "growth_opportunity": intel["rural_opportunity"],
        "capital_assessment": capital_assessment,
    }
