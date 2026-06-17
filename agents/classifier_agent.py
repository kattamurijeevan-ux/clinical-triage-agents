from crewai import Agent, LLM
from dotenv import load_dotenv
import os

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0
)

classifier_agent = Agent(
    role="Clinical Intake Classifier",
    goal="Extract structured clinical information from raw patient intake forms",
    backstory=(
        "You are an experienced triage nurse with years of emergency department experience. "
        "You quickly read intake forms and identify the chief complaint, relevant symptoms, "
        "and any red-flag indicators that need urgent attention. You are precise and never "
        "add information that isn't in the form."
    ),
    llm=llm,
    verbose=True,
    allow_delegation=False
)