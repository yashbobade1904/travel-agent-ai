"""
Budget Estimation Tool
-----------------------
Calculates total estimated trip budget based on
flight cost, hotel cost, and daily local expenses.
"""

from langchain.tools import tool

# Estimated daily food + local travel costs by city (INR)
DAILY_EXPENSE_ESTIMATES = {
    "Goa":       {"budget": 800,  "mid": 1500, "luxury": 3000},
    "Mumbai":    {"budget": 900,  "mid": 1800, "luxury": 4000},
    "Delhi":     {"budget": 700,  "mid": 1400, "luxury": 3500},
    "Bangalore": {"budget": 800,  "mid": 1600, "luxury": 3500},
    "Jaipur":    {"budget": 600,  "mid": 1200, "luxury": 2800},
    "Kolkata":   {"budget": 600,  "mid": 1200, "luxury": 2800},
    "Chennai":   {"budget": 700,  "mid": 1400, "luxury": 3000},
    "Hyderabad": {"budget": 700,  "mid": 1400, "luxury": 3000},
}


@tool
def estimate_budget(query: str) -> str:
    """
    Estimate total trip budget.
    Input format: 'flight:4200 hotel:3200 days:3 city:Goa style:mid'
    Style options: budget, mid, luxury (default: mid).
    Returns full cost breakdown.
    """
    try:
        parts = query.lower().split()
        params = {}
        for part in parts:
            if ":" in part:
                key, val = part.split(":", 1)
                params[key] = val

        flight_cost     = float(params.get("flight", 0))
        hotel_per_night = float(params.get("hotel", 0))
        days            = int(params.get("days", 3))
        city            = params.get("city", "Goa").title()
        style           = params.get("style", "mid").lower()

        hotel_total = hotel_per_night * days

        city_expenses = DAILY_EXPENSE_ESTIMATES.get(
            city, {"budget": 700, "mid": 1500, "luxury": 3000}
        )
        daily_expense     = city_expenses.get(style, city_expenses["mid"])
        food_travel_total = daily_expense * days
        grand_total       = flight_cost + hotel_total + food_travel_total

        result  = f"💰 Budget Breakdown for {days}-Day Trip to {city}:\n\n"
        result += f"  ✈️  Flight:              ₹{flight_cost:,.0f}\n"
        result += f"  🏨  Hotel ({days} nights):    ₹{hotel_total:,.0f}\n"
        result += f"  🍽️  Food & Local Travel: ₹{food_travel_total:,.0f}\n"
        result += f"  {'─'*35}\n"
        result += f"  💳  TOTAL ESTIMATED:     ₹{grand_total:,.0f}\n"
        result += f"\n  (Style: {style.title()} | ~₹{daily_expense}/day for food & travel)"
        return result

    except Exception as e:
        return f"Error estimating budget: {str(e)}"
