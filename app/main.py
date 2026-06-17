from fastapi import FastAPI, HTTPException
from app.models import IntakeForm
from app.database import SessionLocal, TriageRecord
from agents.crew import run_triage
import re
import json

app = FastAPI(
    title="Clinical Triage Agent System",
    version="0.1.0",
    description="Multi-agent CrewAI system for ESI-based clinical intake triage."
)

@app.get("/")
def root():
    return {"service": "Clinical Triage Agent System", "agents": 4, "framework": "CrewAI"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.post("/triage")
def triage_patient(form: IntakeForm):
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

    # Extract ESI level and escalation decision from the final output
    esi_match = re.search(r'ESI level (?:of )?(\d)', result_text)
    esi_level = int(esi_match.group(1)) if esi_match else None

    escalation = "needs_more_info"
    if "urgent" in result_text.lower()[:20]:
        escalation = "urgent"
    elif "routine" in result_text.lower()[:20]:
        escalation = "routine"

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