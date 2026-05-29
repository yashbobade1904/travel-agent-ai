# ✈️ AI Travel Planning Assistant

An **Agentic AI** system that autonomously plans complete travel itineraries using LangChain, Groq (Llama), and real-time weather data.

---

## 🗂️ Project Structure

```
travel_agent/
├── app.py              ← Streamlit web UI (run this)
├── agent.py            ← LangChain ReAct agent (the brain)
├── requirements.txt    ← Python dependencies
├── README.md           ← This file
├── tools/
│   ├── __init__.py     ← Registers all tools
│   ├── flight_tool.py  ← Searches flights.json
│   ├── hotel_tool.py   ← Searches hotels.json
│   ├── places_tool.py  ← Searches places.json
│   ├── weather_tool.py ← Calls Open-Meteo API (free, no key needed)
│   └── budget_tool.py  ← Estimates total trip cost
└── data/
    ├── flights.json    ← Flight data (30 routes)
    ├── hotels.json     ← Hotel data (40 hotels)
    └── places.json     ← Tourist attractions (40 places)
```

---

## 🚀 Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Get a FREE Groq API key
- Go to https://console.groq.com
- Sign up and click "API Keys"
- Click "Create API Key"
- Copy the key (starts with `gsk_...`)
- Completely free, no credit card needed!

### 3. Run the app
```bash
streamlit run app.py
```

### 4. Open browser
```
http://localhost:8501
```

### 5. Enter Groq API key in the sidebar and start planning!

---

## 💬 Example Queries

- `Plan a 3-day trip to Goa from Delhi under ₹20,000`
- `I want a 5-day trip to Jaipur from Mumbai, mid-range budget`
- `Plan a weekend trip to Goa from Bangalore`

---

## 🧠 How It Works (Agentic AI)

The agent uses the **ReAct pattern** (Reasoning + Acting):

```
User Request
    ↓
Agent THINKS: "I need flight info first"
    ↓
Agent CALLS: search_flights("from:Mumbai to:Goa")
    ↓
Agent READS result, THINKS: "Now I need hotel info"
    ↓
Agent CALLS: search_hotels("city:Goa budget:5000")
    ↓
... repeats for weather, places, budget ...
    ↓
Agent GENERATES: Complete formatted itinerary
```

---

## 🌤️ Weather API

Uses **Open-Meteo** — completely free, no API key needed.
URL: https://api.open-meteo.com/v1/forecast

---

## 🤖 AI Model

Uses **Llama 3.3 70B** via Groq API + LangChain + LangGraph.
- Free tier: console.groq.com
- No credit card required

---

## 📝 Coding Standards

- All functions have docstrings
- Error handling via try-except in every tool
- Modular structure: each tool is a separate file
- PEP 8 compliant code
