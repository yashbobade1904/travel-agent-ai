# This file makes 'tools' a Python package.
# Import all tools here so agent.py can import them easily.

from tools.flight_tool import search_flights
from tools.hotel_tool import search_hotels
from tools.places_tool import search_places
from tools.weather_tool import get_weather
from tools.budget_tool import estimate_budget

# Collect all tools in one list for the agent
ALL_TOOLS = [search_flights, search_hotels, search_places, get_weather, estimate_budget]
