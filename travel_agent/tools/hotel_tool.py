"""
Hotel Recommendation Tool
--------------------------
Reads hotels.json and returns best hotels in a city.
Data format:
{
  "hotel_id": "HOT0001",
  "name": "Grand Palace Hotel",
  "city": "Delhi",
  "stars": 4,
  "price_per_night": 3897,
  "amenities": ["wifi", "pool"]
}
"""

import json
import os
from langchain.tools import tool

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "hotels.json")


@tool
def search_hotels(query: str) -> str:
    """
    Search for hotels in a city with optional budget filter.
    Input format: 'city:Goa budget:5000'
    Budget is optional (max price per night in INR).
    Returns top hotels sorted by star rating.
    """
    try:
        parts = query.lower().split()
        city = None
        max_budget = float("inf")

        for part in parts:
            if part.startswith("city:"):
                city = part.split("city:")[1].strip().title()
            elif part.startswith("budget:"):
                max_budget = float(part.split("budget:")[1].strip())

        if not city:
            return "Please provide a city. Format: 'city:Goa budget:5000'"

        with open(DATA_PATH, "r") as f:
            hotels = json.load(f)

        matches = [
            h for h in hotels
            if h["city"].lower() == city.lower()
            and h["price_per_night"] <= max_budget
        ]

        if not matches:
            return f"No hotels found in {city} within budget ₹{max_budget:,.0f}."

        # Sort by stars (highest first), then by price (lowest first)
        matches.sort(key=lambda x: (-x["stars"], x["price_per_night"]))

        result = f"🏨 Hotels in {city}:\n\n"
        for i, h in enumerate(matches[:4], 1):
            amenities = ", ".join(h["amenities"][:3])
            stars_str = "⭐" * h["stars"]
            result += (
                f"{i}. {h['name']} | {stars_str} | "
                f"₹{h['price_per_night']:,}/night | "
                f"Amenities: {amenities}\n"
            )

        best = matches[0]
        result += (
            f"\n✅ RECOMMENDED: {best['name']} "
            f"({'⭐' * best['stars']}, ₹{best['price_per_night']:,}/night)"
        )
        return result

    except Exception as e:
        return f"Error searching hotels: {str(e)}"
