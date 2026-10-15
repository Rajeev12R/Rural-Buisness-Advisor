
from decimal import Decimal


def calculate_monthly_profit(revenue, expenses):
    revenue = Decimal(str(revenue))
    expenses = Decimal(str(expenses))

    return revenue - expenses


def calculate_break_even_sales(fixed_costs, variable_cost_ratio):
    fixed_costs = Decimal(str(fixed_costs))
    variable_cost_ratio = Decimal(str(variable_cost_ratio))

    if fixed_costs < 0:
        raise ValueError("Fixed costs cannot be negative.")

    if not Decimal("0") <= variable_cost_ratio < Decimal("1"):
        raise ValueError(
            "Variable cost ratio must be between 0 and 1."
        )

    contribution_margin = Decimal("1") - variable_cost_ratio

    return fixed_costs / contribution_margin


def calculate_loan_emi(principal, annual_interest_rate, months):
    principal = Decimal(str(principal))
    annual_interest_rate = Decimal(str(annual_interest_rate))

    if principal <= 0:
        raise ValueError("Loan amount must be greater than zero.")

    if annual_interest_rate < 0:
        raise ValueError("Interest rate cannot be negative.")

    if months <= 0:
        raise ValueError("Loan tenure must be greater than zero.")

    monthly_rate = annual_interest_rate / Decimal("1200")

    if monthly_rate == 0:
        return principal / Decimal(months)

    factor = (Decimal("1") + monthly_rate) ** months

    return (
        principal * monthly_rate * factor / (factor - Decimal("1"))
    )


def calculate_profit_margin(revenue, profit):
    revenue = Decimal(str(revenue))
    profit = Decimal(str(profit))

    if revenue <= 0:
        return None

    return (profit / revenue) * Decimal("100")


def calculate_emi_to_revenue_ratio(emi, revenue):
    revenue = Decimal(str(revenue))
    emi = Decimal(str(emi))

    if revenue <= 0:
        return None

    return (emi / revenue) * Decimal("100")
