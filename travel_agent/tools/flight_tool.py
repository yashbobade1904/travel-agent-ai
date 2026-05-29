"""
Flight Search Tool
------------------
Reads flights.json and finds available flights between two cities.
Data format:
{
  "flight_id": "FL0001",
  "airline": "IndiGo",
  "from": "Delhi",
  "to": "Goa",
  "departure_time": "2025-01-04T14:00:00",
  "arrival_time": "2025-01-04T16:30:00",
  "price": 4800
}
"""

import json
import os
from datetime import datetime
from langchain.tools import tool

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "flights.json")


@tool
def search_flights(query: str) -> str:
    """
    Search for available flights between two cities.
    Input format: 'from:Delhi to:Goa'
    Returns cheapest flight options with departure/arrival times.
    """
    try:
        parts = query.lower().split()
        origin, destination = None, None

        for part in parts:
            if part.startswith("from:"):
                origin = part.split("from:")[1].strip().title()
            elif part.startswith("to:"):
                destination = part.split("to:")[1].strip().title()

        if not origin or not destination:
            return "Please provide origin and destination. Format: 'from:Delhi to:Goa'"

        with open(DATA_PATH, "r") as f:
            flights = json.load(f)

        matches = [
            fl for fl in flights
            if fl["from"].lower() == origin.lower()
            and fl["to"].lower() == destination.lower()
        ]

        if not matches:
            return f"No direct flights found from {origin} to {destination}."

        # Sort by price (cheapest first)
        matches.sort(key=lambda x: x["price"])

        def fmt_time(dt_str):
            """Format ISO datetime to readable time string."""
            try:
                dt = datetime.fromisoformat(dt_str)
                return dt.strftime("%I:%M %p")
            except:
                return dt_str

        result = f"✈️ Flights from {origin} to {destination}:\n\n"
        for i, fl in enumerate(matches[:3], 1):
            dep = fmt_time(fl["departure_time"])
            arr = fmt_time(fl["arrival_time"])
            result += (
                f"{i}. {fl['airline']} | ₹{fl['price']:,} | "
                f"Departs {dep} → Arrives {arr} | ID: {fl['flight_id']}\n"
            )

        best = matches[0]
        result += f"\n✅ RECOMMENDED: {best['airline']} at ₹{best['price']:,} (cheapest), departs {fmt_time(best['departure_time'])}"
        return result

    except Exception as e:
        return f"Error searching flights: {str(e)}"
