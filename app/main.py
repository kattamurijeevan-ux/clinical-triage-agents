from fastapi import FastAPI, HTTPException
from app.models import IntakeForm
from app.database import SessionLocal, TriageRecord
from agents.crew import run_triage
import re

app = FastAPI(
    title="Clinical Triage Agent System",
    version="0.1.0",
    description="Multi-agent CrewAI system for ESI-based clinical intake triage."
)

def is_vague_input(form: IntakeForm) -> bool:
    combined = f"{form.chief_complaint} {form.symptoms}".strip().lower()
    word_count = len(combined.split())
    vague_phrases = ["not feeling well", "hurts somewhere", "tired", "pain", "don't feel good"]
    return word_count <= 4 or combined in vague_phrases

def extract_esi_and_escalation(result_text: str):
    esi_match = re.search(r'ESI\s*level[:\s]*(?:of\s*)?(\d)', result_text, re.IGNORECASE)
    esi_level = int(esi_match.group(1)) if esi_match else None

    text_lower = result_text.lower()
    first_30 = text_lower[:30]

    if "needs_more_info" in text_lower or "needs more info" in first_30:
        escalation = "needs_more_info"
    elif "urgent" in first_30:
        escalation = "urgent"
    elif "routine" in first_30:
        escalation = "routine"
    else:
        escalation = "unknown"

    return esi_level, escalation

@app.get("/")
def root():
    return {"service": "Clinical Triage Agent System", "agents": 4, "framework": "CrewAI"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/triage")
def triage_patient(form: IntakeForm):
    # Guard: vague inputs get flagged before ever reaching the agents
    if is_vague_input(form):
        db = SessionLocal()
        record = TriageRecord(
            patient_id=form.patient_id,
            chief_complaint=form.chief_complaint,
            esi_level=None,
            escalation="needs_more_info",
            confidence=0.0,
            agent_trace="Flagged by input guard: insufficient detail to assess severity."
        )
        db.add(record)
        db.commit()
        db.close()
        return {
            "patient_id": form.patient_id,
            "esi_level": None,
            "escalation": "needs_more_info",
            "full_reasoning": "Input too vague to triage safely. Please provide more specific symptoms, duration, and vital signs."
        }

    intake_text = f"""
Chief complaint: {form.chief_complaint}
Symptoms: {form.symptoms}
History: {form.history}
Vitals: {form.vitals}
"""

    try:
        result = run_triage(intake_text)
        result_text = str(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    esi_level, escalation = extract_esi_and_escalation(result_text)

    db = SessionLocal()
    record = TriageRecord(
        patient_id=form.patient_id,
        chief_complaint=form.chief_complaint,
        esi_level=esi_level,
        escalation=escalation,
        confidence=0.0,
        agent_trace=result_text
    )
    db.add(record)
    db.commit()
    db.close()

    return {
        "patient_id": form.patient_id,
        "esi_level": esi_level,
        "escalation": escalation,
        "full_reasoning": result_text
    }

@app.get("/triage/history")
def get_history():
    db = SessionLocal()
    records = db.query(TriageRecord).order_by(TriageRecord.created_at.desc()).limit(50).all()
    db.close()
    return [
        {
            "patient_id": r.patient_id,
            "esi_level": r.esi_level,
            "escalation": r.escalation,
            "created_at": str(r.created_at)
        }
        for r in records
    ]