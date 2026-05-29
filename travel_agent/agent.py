from langchain_groq import ChatGroq
from langgraph.prebuilt import create_react_agent
from tools import ALL_TOOLS

SYSTEM_PROMPT = """You are an expert AI Travel Planning Assistant for Indian destinations.
Use these tools one by one:
1. search_flights - input exactly like: from:Mumbai to:Goa
2. search_hotels - input exactly like: city:Goa budget:5000
3. search_places - input exactly like: city:Goa
4. get_weather - input exactly like: city:Goa days:3
5. estimate_budget - input exactly like: flight:3304 hotel:1232 days:3 city:Goa style:budget

After using all tools, write the Final Answer with:
Trip Summary, Flight Selected, Hotel Recommended, Weather Forecast, Day-wise Itinerary, Budget Breakdown."""

def create_travel_agent(api_key):
    llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0, api_key=api_key)
    return create_react_agent(model=llm, tools=ALL_TOOLS, prompt=SYSTEM_PROMPT)

def plan_trip(user_request, api_key):
    try:
        agent = create_travel_agent(api_key)
        result = agent.invoke({"messages": [{"role": "user", "content": user_request}]})
        return result["messages"][-1].content
    except Exception as e:
        return f"Error planning trip: {str(e)}"