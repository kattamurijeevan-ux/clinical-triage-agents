from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

summarizer_agent = Agent(
    role="Clinical Summarizer",
    goal="Write a concise, scannable summary for the provider reviewing this case",
    backstory=(
        "You are a clinical documentation specialist. You write summaries that a busy provider "
        "can read in under 10 seconds and immediately understand the situation. You include only "
        "the chief complaint, key findings, and the assigned ESI level. No filler language."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)