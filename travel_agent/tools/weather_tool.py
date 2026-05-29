"""
Weather Lookup Tool
--------------------
Calls the FREE Open-Meteo API (no API key needed).
Supports all 8 cities present in the actual dataset.
"""

import requests
from langchain.tools import tool

# All cities from the actual dataset
CITY_COORDS = {
    "Goa":       (15.2993, 74.1240),
    "Mumbai":    (19.0760, 72.8777),
    "Delhi":     (28.7041, 77.1025),
    "Bangalore": (12.9716, 77.5946),
    "Jaipur":    (26.9124, 75.7873),
    "Kolkata":   (22.5726, 88.3639),
    "Chennai":   (13.0827, 80.2707),
    "Hyderabad": (17.3850, 78.4867),
}

WEATHER_CODES = {
    0: "☀️ Clear sky",
    1: "🌤️ Mainly clear", 2: "⛅ Partly cloudy", 3: "☁️ Overcast",
    45: "🌫️ Foggy", 48: "🌫️ Icy fog",
    51: "🌦️ Light drizzle", 61: "🌧️ Light rain", 63: "🌧️ Moderate rain",
    71: "❄️ Light snow", 80: "🌦️ Rain showers", 95: "⛈️ Thunderstorm",
}


@tool
def get_weather(query: str) -> str:
    """
    Get weather forecast for a city for the next few days.
    Input format: 'city:Goa days:3'
    Supported cities: Goa, Mumbai, Delhi, Bangalore, Jaipur, Kolkata, Chennai, Hyderabad.
    Uses the free Open-Meteo API — no API key needed.
    """
    try:
        parts = query.lower().split()
        city, days = None, 3

        for part in parts:
            if part.startswith("city:"):
                city = part.split("city:")[1].strip().title()
            elif part.startswith("days:"):
                days = int(part.split("days:")[1].strip())

        if not city:
            return "Please provide a city. Format: 'city:Goa days:3'"

        coords = CITY_COORDS.get(city)
        if not coords:
            # Fallback: Open-Meteo geocoding
            geo = requests.get(
                f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1",
                timeout=10
            ).json()
            if not geo.get("results"):
                return f"Could not find coordinates for {city}."
            coords = (geo["results"][0]["latitude"], geo["results"][0]["longitude"])

        lat, lon = coords
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}&longitude={lon}"
            f"&daily=temperature_2m_max,temperature_2m_min,weather_code"
            f"&timezone=auto&forecast_days={days}"
        )
        data = requests.get(url, timeout=10).json()
        daily = data.get("daily", {})
        dates     = daily.get("time", [])
        max_temps = daily.get("temperature_2m_max", [])
        min_temps = daily.get("temperature_2m_min", [])
        codes     = daily.get("weather_code", [])

        result = f"🌤️ Weather Forecast for {city} ({days} days):\n\n"
        for i in range(len(dates)):
            desc = WEATHER_CODES.get(codes[i], "🌡️ Variable")
            result += (
                f"Day {i+1} ({dates[i]}): {desc} | "
                f"🌡️ {min_temps[i]}°C – {max_temps[i]}°C\n"
            )
        return result

    except requests.exceptions.RequestException as e:
        return f"Weather API error: {str(e)}"
    except Exception as e:
        return f"Error fetching weather: {str(e)}"
