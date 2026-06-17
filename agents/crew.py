# Workaround for CrewAI bug #5886 — cache_breakpoint injected for non-Anthropic providers
import crewai.llms.cache as _crewai_cache
_crewai_cache.mark_cache_breakpoint = lambda msg: msg

from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY", "")

from crewai import Crew, Process
from agents.classifier_agent import classifier_agent
from agents.risk_agent import risk_agent
from agents.summarizer_agent import summarizer_agent
from agents.escalation_agent import escalation_agent
from tasks.triage_tasks import build_tasks

def run_triage(intake_text: str):
    tasks = build_tasks(intake_text)

    crew = Crew(
        agents=[classifier_agent, risk_agent, summarizer_agent, escalation_agent],
        tasks=tasks,
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff()
    return result