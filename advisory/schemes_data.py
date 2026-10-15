"""Verified Government Schemes and Financing Options for Rural Micro-Entrepreneurs.

Contains scheme criteria, subsidy calculations, required documentation, and application steps.
"""

from typing import Any

SCHEME_REGISTRY: list[dict[str, Any]] = [
    {
        "id": "pmegp",
        "name": "Prime Minister's Employment Generation Programme (PMEGP)",
        "ministry": "Ministry of Micro, Small and Medium Enterprises (MSME) & KVIC",
        "applicable_sectors": ["grocery", "dairy", "tailoring", "handicraft", "agriculture", "other"],
        "max_project_cost": 5000000,  # ₹50 Lakh for manufacturing, ₹20 Lakh for business/service
        "subsidy_details": "Rural Area Subsidy: 25% for General category, 35% for Special categories (SC/ST/OBC/Women/Ex-servicemen/Minorities). Own contribution only 5-10%.",
        "loan_type": "Composite Term Loan + Working Capital from nationalized and regional rural banks.",
        "key_eligibility": [
            "Any individual above 18 years of age.",
            "For projects above ₹10 Lakh in manufacturing or ₹5 Lakh in service, minimum 8th standard pass is required.",
            "New micro-enterprises only.",
        ],
        "required_documents": [
            "Aadhaar Card and PAN Card",
            "Rural Area Residence / Domicile Certificate from Gram Panchayat / Tehsildar",
            "Special Category Certificate (if claiming 35% subsidy)",
            "Detailed Project Report (DPR) / Cost Estimates",
            "Educational Qualification Certificate (if project > ₹5L / ₹10L)",
            "Machinery / Equipment Quotations",
        ],
        "application_process": "Apply 100% online through the PMEGP e-Portal (kviconline.gov.in/pmegpep) or via national JanSamarth portal. No paper application needed.",
        "official_portal": "https://www.kviconline.gov.in/pmegpep/",
    },
    {
        "id": "mudra",
        "name": "Pradhan Mantri MUDRA Yojana (PMMY)",
        "ministry": "Department of Financial Services, Ministry of Finance",
        "applicable_sectors": ["grocery", "dairy", "tailoring", "handicraft", "agriculture", "other"],
        "max_project_cost": 1000000,  # Up to ₹10 Lakh (₹20 Lakh under enhanced 2024 guidelines)
        "subsidy_details": "Collateral-free institutional credit. Interest rates linked to bank base rates (typically 8.5% - 11.5% p.a.). Zero processing fee for Shishu category.",
        "loan_type": "Collateral-free Micro Business Loan with Mudra RuPay Debit Card for working capital.",
        "categories": [
            "Shishu: Loans up to ₹50,000 (ideal for micro-stalls, initial sewing machine, small kirana seed stock)",
            "Kishore: Loans from ₹50,001 to ₹5,00,000 (ideal for business expansion and inventory)",
            "Tarun: Loans from ₹5,00,001 to ₹10,00,000 (for established units scaling operations)",
        ],
        "key_eligibility": [
            "Non-corporate small business segment (proprietorship, partnership, small rural firm).",
            "No prior loan default with any commercial or cooperative bank.",
        ],
        "required_documents": [
            "Identity proof (Aadhaar / Voter ID / Driving License)",
            "Proof of residence (Panchayat certificate / electricity bill / ration card)",
            "Business address proof and trade registration / Udyam registration",
            "Quotation of machinery / items to be purchased",
            "Passport-size photographs",
        ],
        "application_process": "Apply through any nearby Commercial Bank, Regional Rural Bank (RRB), Small Finance Bank, or online at udyamimitra.in.",
        "official_portal": "https://www.mudra.org.in/",
    },
    {
        "id": "kcc_animal_husbandry",
        "name": "Kisan Credit Card (KCC) for Animal Husbandry & Dairy",
        "ministry": "Ministry of Fisheries, Animal Husbandry and Dairying",
        "applicable_sectors": ["dairy", "agriculture"],
        "max_project_cost": 300000,  # Up to ₹3 Lakh (₹2 Lakh collateral-free)
        "subsidy_details": "Concessional interest rate of 7% p.a. with an additional 3% prompt repayment incentive (effective net interest rate only 4% p.a.).",
        "loan_type": "Revolving Cash Credit facility for feed, veterinary medicines, breeding, and labor.",
        "key_eligibility": [
            "Dairy farmers owning or leasing milch cattle/buffaloes, individuals, or SHG/JLGs.",
            "Can be availed without land mortgage up to ₹1.6 Lakh to ₹2.0 Lakh.",
        ],
        "required_documents": [
            "Aadhaar Card and Land Record (or cattle ownership certificate / milk union passbook)",
            "Bank account passbook",
            "Health & vaccination certificate of livestock from local veterinary officer",
        ],
        "application_process": "Submit KCC Animal Husbandry application form at your local bank branch, Dairy Cooperative Society, or Common Service Centre (CSC).",
        "official_portal": "https://dahd.nic.in/",
    },
    {
        "id": "pmfme",
        "name": "PM Formalisation of Micro food processing Enterprises (PMFME)",
        "ministry": "Ministry of Food Processing Industries (MoFPI)",
        "applicable_sectors": ["agriculture", "dairy"],
        "max_project_cost": 3000000,
        "subsidy_details": "Credit-linked capital subsidy at 35% of eligible project cost with a ceiling of ₹10 Lakh per unit. Seed capital of ₹40,000 for SHG members.",
        "loan_type": "Term loan + capital subsidy credited directly to bank loan account.",
        "key_eligibility": [
            "Micro food processing units (flour mills, spice grinding, dairy products like ghee/paneer, pickle making, oil extraction).",
            "Existing or new units in rural areas.",
        ],
        "required_documents": [
            "Aadhaar and PAN Card",
            "Project Report detailing food processing machinery and capacity",
            "FSSAI basic registration (can be obtained post-approval)",
            "Bank statement and electricity connection proof",
        ],
        "application_process": "Register online via the PMFME portal with District Resource Person (DRP) guidance.",
        "official_portal": "https://pmfme.mofpi.gov.in/",
    },
    {
        "id": "kvic_gramodyog",
        "name": "Gramodyog Vikas Yojana (Rural Crafts & Artisans)",
        "ministry": "Khadi and Village Industries Commission (KVIC)",
        "applicable_sectors": ["tailoring", "handicraft"],
        "max_project_cost": 500000,
        "subsidy_details": "Free skill training, subsidized modern toolkit distribution (motorized sewing machines, pottery wheels, artisan toolkits), and exhibition marketing support.",
        "loan_type": "Tool kit grant + linkage with MUDRA bank financing.",
        "key_eligibility": [
            "Traditional rural artisans, tailors, potters, weavers, and self-employed youth.",
            "Preference given to rural women and marginalized communities.",
        ],
        "required_documents": [
            "Aadhaar card",
            "Artisan card or Panchayat certificate verifying craft occupation",
            "Bank passbook",
        ],
        "application_process": "Apply through District KVIC office, District Industries Centre (DIC), or online at kviconline.gov.in.",
        "official_portal": "https://www.kvic.gov.in/",
    },
]


def match_government_schemes(
    business_type: str,
    loan_amount: float = 0,
    available_capital: float = 0,
    state: str = "Punjab",
) -> list[dict[str, Any]]:
    """Matches the entrepreneur's profile and financing need to relevant government schemes."""
    b_type = (business_type or "other").lower().strip()
    total_financing_need = loan_amount if loan_amount > 0 else available_capital

    matched: list[dict[str, Any]] = []

    for scheme in SCHEME_REGISTRY:
        # Check sector suitability
        if b_type in scheme["applicable_sectors"] or "other" in scheme["applicable_sectors"]:
            is_recommended = False
            match_reason = ""

            # Check specific scheme suitability
            if scheme["id"] == "pmegp":
                is_recommended = total_financing_need >= 50000
                match_reason = (
                    "Best for obtaining up to 35% capital subsidy on new business setups in rural areas."
                )
            elif scheme["id"] == "mudra":
                is_recommended = True
                if total_financing_need <= 50000:
                    tier = "Shishu (up to ₹50,000, 0% collateral, fast disbursal)"
                elif total_financing_need <= 500000:
                    tier = "Kishore (₹50k - ₹5 Lakh, suitable for your setup scale)"
                else:
                    tier = "Tarun (₹5 Lakh - ₹10 Lakh)"
                match_reason = f"Ideal collateral-free loan tier: {tier}."
            elif scheme["id"] == "kcc_animal_husbandry" and b_type in ("dairy", "agriculture"):
                is_recommended = True
                match_reason = (
                    "Highly recommended for dairy working capital: subsidized 4% net interest rate."
                )
            elif scheme["id"] == "pmfme" and b_type in ("dairy", "agriculture"):
                is_recommended = total_financing_need >= 100000
                match_reason = (
                    "Excellent 35% capital subsidy for food processing & dairy value-addition."
                )
            elif scheme["id"] == "kvic_gramodyog" and b_type in ("tailoring", "handicraft"):
                is_recommended = True
                match_reason = (
                    "Provides free modern toolkits, specialized training, and exhibition marketing access."
                )

            matched.append({
                "id": scheme["id"],
                "name": scheme["name"],
                "ministry": scheme["ministry"],
                "is_recommended": is_recommended,
                "match_reason": match_reason,
                "subsidy_details": scheme["subsidy_details"],
                "loan_type": scheme["loan_type"],
                "key_eligibility": scheme["key_eligibility"],
                "required_documents": scheme["required_documents"],
                "application_process": scheme["application_process"],
                "official_portal": scheme["official_portal"],
            })

    # Sort so recommended schemes appear first
    matched.sort(key=lambda s: not s["is_recommended"])
    return matched
