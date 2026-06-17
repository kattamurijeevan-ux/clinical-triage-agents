from pydantic import BaseModel
from typing import Optional

class IntakeForm(BaseModel):
    patient_id: str
    chief_complaint: str
    symptoms: str
    vitals: Optional[str] = ""
    history: Optional[str] = ""

class TriageResult(BaseModel):
    patient_id: str
    esi_level: int
    classification: str
    risk_summary: str
    provider_summary: str
    escalation: str
    confidence: float
    agent_trace: list