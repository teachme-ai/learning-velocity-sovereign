"""
Currency Converter Skill — converts USD costs to INR (and vice versa).
Used by the factory pipeline for cost reporting in dual currencies.

Usage:
    from .currency_converter import convert_usd_to_inr, convert_inr_to_usd, format_dual_cost

    # Single conversion
    inr = convert_usd_to_inr(0.05)  # => 4.25

    # Format for display
    print(format_dual_cost(0.05))  # => "$0.0500 (₹4.2500)"

    # Convert a full cost report
    report = enrich_report_with_inr(cost_report_dict)
"""

# Approximate rate — update periodically or fetch live
USD_TO_INR = 85.0


def convert_usd_to_inr(usd_amount, rate=None):
    """Convert USD to INR."""
    r = rate or USD_TO_INR
    return round(usd_amount * r, 4)


def convert_inr_to_usd(inr_amount, rate=None):
    """Convert INR to USD."""
    r = rate or USD_TO_INR
    return round(inr_amount / r, 6)


def format_dual_cost(usd_amount, rate=None):
    """Format a USD amount as '$X.XXXX (₹Y.YYYY)'."""
    inr = convert_usd_to_inr(usd_amount, rate)
    return f"${usd_amount:.4f} (₹{inr:.4f})"


def enrich_report_with_inr(report, rate=None):
    """
    Take a cost_report dict (from CostTracker.report()) and add INR fields
    wherever USD fields exist. Returns the enriched dict.
    """
    r = rate or USD_TO_INR
    if "total_cost_usd" in report and "total_cost_inr" not in report:
        report["total_cost_inr"] = round(report["total_cost_usd"] * r, 4)
    if "by_task" in report:
        for task, data in report["by_task"].items():
            if "cost_usd" in data and "cost_inr" not in data:
                data["cost_inr"] = round(data["cost_usd"] * r, 4)
            elif "cost" in data and "cost_inr" not in data:
                data["cost_inr"] = round(data["cost"] * r, 4)
    return report
