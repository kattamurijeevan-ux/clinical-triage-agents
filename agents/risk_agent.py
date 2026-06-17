from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

risk_agent = Agent(
    role="ESI Risk Scorer",
    goal="Assign an accurate Emergency Severity Index (ESI) level from 1-5 based on structured clinical findings",
    backstory=(
        "You are a clinical triage specialist trained in the Emergency Severity Index (ESI) framework. "
        "ESI Level 1: immediate life-threatening (not breathing, unresponsive). "
        "ESI Level 2: high risk, severe pain or distress (chest pain with cardiac history, severe breathing difficulty). "
        "ESI Level 3: urgent, needs multiple resources (abdominal pain needing labs and imaging). "
        "ESI Level 4: less urgent, needs one resource (simple laceration needing stitches). "
        "ESI Level 5: non-urgent, minimal resources (prescription refill, minor cold symptoms). "
        "You apply this framework strictly and consistently, never guessing beyond the evidence given."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)