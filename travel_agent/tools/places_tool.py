"""
Places Discovery Tool
----------------------
Reads places.json and recommends top attractions in a city.
Data format:
{
  "place_id": "PLC0001",
  "name": "Famous Fort",
  "city": "Delhi",
  "type": "fort",
  "rating": 4.6
}
"""

import json
import os
from langchain.tools import tool

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "places.json")


@tool
def search_places(query: str) -> str:
    """
    Find tourist attractions in a city.
    Input format: 'city:Goa type:beach'
    Type is optional. Common types: fort, temple, museum, park, beach, lake, market, monument.
    Returns top-rated places sorted by rating.
    """
    try:
        parts = query.lower().split()
        city = None
        place_type = None

        for part in parts:
            if part.startswith("city:"):
                city = part.split("city:")[1].strip().title()
            elif part.startswith("type:"):
                place_type = part.split("type:")[1].strip().lower()

        if not city:
            return "Please provide a city. Format: 'city:Goa'"

        with open(DATA_PATH, "r") as f:
            places = json.load(f)

        matches = [p for p in places if p["city"].lower() == city.lower()]

        if place_type:
            matches = [p for p in matches if p["type"].lower() == place_type]

        if not matches:
            return f"No places found in {city}."

        # Sort by rating (highest first)
        matches.sort(key=lambda x: x["rating"], reverse=True)

        result = f"📍 Top Attractions in {city}"
        if place_type:
            result += f" (type: {place_type})"
        result += ":\n\n"

        for i, p in enumerate(matches[:6], 1):
            result += (
                f"{i}. {p['name']} | ⭐ {p['rating']} | "
                f"Type: {p['type'].title()} | ID: {p['place_id']}\n"
            )

        return result

    except Exception as e:
        return f"Error searching places: {str(e)}"
