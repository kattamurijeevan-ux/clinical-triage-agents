from crewai import Task
from agents.classifier_agent import classifier_agent
from agents.risk_agent import risk_agent
from agents.summarizer_agent import summarizer_agent
from agents.escalation_agent import escalation_agent

def build_tasks(intake_text: str):

    classify_task = Task(
        description=(
            f"Read this patient intake form and extract the chief complaint, symptoms, "
            f"and any vitals or history mentioned. Be precise — do not infer anything not stated.\n\n"
            f"Intake form:\n{intake_text}"
        ),
        expected_output="A structured summary of chief complaint, symptoms, vitals, and history.",
        agent=classifier_agent
    )

    risk_task = Task(
        description=(
            "Using the structured clinical findings from the previous step, assign an ESI level "
            "from 1 to 5 following the ESI framework strictly. State the ESI level as a single number "
            "and explain your reasoning in one sentence."
        ),
        expected_output="ESI level (1-5) with a one-sentence justification.",
        agent=risk_agent,
        context=[classify_task]
    )

    summarize_task = Task(
        description=(
            "Write a concise provider-facing summary using the classification and ESI level from "
            "previous steps. Maximum 3 sentences."
        ),
        expected_output="A 2-3 sentence clinical summary for the provider.",
        agent=summarizer_agent,
        context=[classify_task, risk_task]
    )

    escalation_task = Task(
        description=(
            "Based on the ESI level and summary, decide the final routing. Respond with exactly one "
            "of: 'urgent', 'routine', or 'needs_more_info'. Then give a one-sentence reason."
        ),
        expected_output="One word routing decision (urgent/routine/needs_more_info) with a one-sentence reason.",
        agent=escalation_agent,
        context=[classify_task, risk_task, summarize_task]
    )

    return [classify_task, risk_task, summarize_task, escalation_task]