"""
Streamlit Web Application
--------------------------
This file creates the web UI for the Travel Planning Agent.

Streamlit works like this:
- You write Python code that describes the UI
- Every time the user clicks or types, Streamlit re-runs this file top to bottom
- Session state (st.session_state) remembers things between re-runs

Run with: streamlit run app.py
"""

import streamlit as st
import os
import sys

# Make sure Python can find our tools and agent modules
sys.path.insert(0, os.path.dirname(__file__))

from agent import plan_trip

# ── Page Configuration ─────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS Styling ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=DM+Sans:wght@400;500&display=swap');

    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #f0f0f0;
    }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3rem;
        text-align: center;
        background: linear-gradient(90deg, #f7c59f, #EB8258);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        font-family: 'DM Sans', sans-serif;
        text-align: center;
        color: #a0c4c4;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }

    section[data-testid="stSidebar"] {
        background: rgba(15, 32, 39, 0.9);
        border-right: 1px solid rgba(247, 197, 159, 0.2);
    }

    textarea {
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid rgba(247, 197, 159, 0.4) !important;
        color: #f0f0f0 !important;
        border-radius: 8px !important;
        font-family: 'DM Sans', sans-serif !important;
    }

    .stButton > button {
        background: linear-gradient(90deg, #EB8258, #f7c59f);
        color: #0f2027;
        font-weight: 700;
        font-family: 'DM Sans', sans-serif;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 2rem;
        font-size: 1rem;
        width: 100%;
        transition: transform 0.2s;
    }

    .stButton > button:hover {
        transform: scale(1.03);
    }

    .itinerary-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(247, 197, 159, 0.3);
        border-radius: 12px;
        padding: 2rem;
        font-family: 'DM Sans', sans-serif;
        white-space: pre-wrap;
        line-height: 1.7;
        color: #e8e8e8;
    }

    .example-pill {
        background: rgba(235, 130, 88, 0.15);
        border: 1px solid rgba(235, 130, 88, 0.4);
        border-radius: 20px;
        padding: 0.3rem 0.8rem;
        font-size: 0.85rem;
        color: #f7c59f;
        display: inline-block;
        margin: 0.2rem;
    }
</style>
""", unsafe_allow_html=True)


# ── Initialize Session State ───────────────────────────────────────────────────
if "itinerary" not in st.session_state:
    st.session_state.itinerary = None
if "is_loading" not in st.session_state:
    st.session_state.is_loading = False


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    # API Key input (password-masked for security)
    api_key = st.text_input(
       "🔑 API Key (Groq/Gemini)",
        type="password",
       placeholder="gsk_... or AIza...",
help="Groq: console.groq.com | Gemini: aistudio.google.com"
    )

    st.markdown("---")
    st.markdown("### 🌍 Supported Cities")
    cities = ["Delhi", "Mumbai", "Bangalore", "Goa", "Jaipur", "Kolkata"]
    for city in cities:
        st.markdown(f"• {city}")

    st.markdown("---")
    st.markdown("### 🛠️ Tools Available")
    tools_info = [
        ("✈️", "Flight Search"),
        ("🏨", "Hotel Finder"),
        ("📍", "Places Discovery"),
        ("🌤️", "Live Weather"),
        ("💰", "Budget Calculator"),
    ]
    for icon, name in tools_info:
        st.markdown(f"{icon} {name}")

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.75rem; color:#666;'>Powered by LangChain + Groq Llama 3.3 70B + Open-Meteo</div>",
        unsafe_allow_html=True
    )


# ── Main Page ──────────────────────────────────────────────────────────────────
st.markdown('<h1 class="main-title">✈️ AI Travel Planner</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Powered by Agentic AI — just tell me where you want to go</p>', unsafe_allow_html=True)

# ── Example queries ────────────────────────────────────────────────────────────
st.markdown("**💡 Try asking:**")
examples = [
    "Plan a 3-day trip to Goa from Delhi under ₹20,000",
    "I want a 5-day trip to Jaipur from Mumbai, mid-range budget",
    "Plan a 2-day weekend getaway to Goa from Bangalore",
]
cols = st.columns(len(examples))
for col, ex in zip(cols, examples):
    with col:
        st.markdown(f'<div class="example-pill">{ex}</div>', unsafe_allow_html=True)

st.markdown("---")

# ── Main Input Area ────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 1])

with col1:
    user_query = st.text_area(
        "🗺️ Describe your trip:",
        placeholder="e.g. Plan a 4-day trip to Goa from Delhi. My budget is ₹25,000. I like beaches and local food.",
        height=120,
        key="trip_query"
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    days = st.slider("📅 Trip Duration (days)", min_value=1, max_value=7, value=3)
    travel_style = st.selectbox("🎒 Travel Style", ["Budget", "Mid-range", "Luxury"])

# ── Generate Button ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])

with btn_col2:
    generate_clicked = st.button("🚀 Plan My Trip!", use_container_width=True)


# ── Handle Button Click ────────────────────────────────────────────────────────
if generate_clicked:
    if not api_key:
        st.error("❌ Please enter your Groq API key in the sidebar.")
    elif not user_query.strip():
        st.error("❌ Please describe your trip first.")
    else:
        full_query = f"{user_query.strip()} Duration: {days} days. Travel style: {travel_style}."

        with st.spinner("🤖 Your AI travel agent is researching flights, hotels, weather, and attractions..."):
            itinerary = plan_trip(full_query, api_key)
            if isinstance(itinerary, list):
                itinerary = " ".join([item.get("text", str(item)) for item in itinerary if isinstance(item, dict)])
            st.session_state.itinerary = str(itinerary)


# ── Display the Itinerary ──────────────────────────────────────────────────────
if st.session_state.itinerary:
    st.markdown("---")
    st.markdown("## 📋 Your Personalized Travel Itinerary")

    st.markdown(
        f'<div class="itinerary-box">{st.session_state.itinerary}</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        label="⬇️ Download Itinerary",
        data=st.session_state.itinerary,
        file_name="my_travel_itinerary.txt",
        mime="text/plain"
    )

    if st.button("🔄 Plan Another Trip"):
        st.session_state.itinerary = None
        st.rerun()


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<div style='text-align:center; color:#555; font-size:0.8rem;'>"
    "AI Travel Planner • Built with LangChain, Streamlit & Open-Meteo API"
    "</div>",
    unsafe_allow_html=True
)
