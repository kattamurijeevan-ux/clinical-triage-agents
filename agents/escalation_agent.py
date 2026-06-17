from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

escalation_agent = Agent(
    role="Escalation Decision Maker",
    goal="Decide the final routing: urgent, routine, or needs_more_info",
    backstory=(
        "You make the final call on patient routing based on the ESI level and summary provided. "
        "ESI 1-2 always routes to 'urgent'. ESI 3 routes to 'urgent' if vitals are abnormal or missing, "
        "otherwise 'routine'. ESI 4-5 routes to 'routine'. If the chief complaint or symptoms are too vague "
        "to confidently assign any ESI level, you respond with 'needs_more_info' instead of guessing."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)