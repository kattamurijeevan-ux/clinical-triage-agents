from sqlalchemy import create_engine, Column, String, Float, Integer, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import uuid

engine = create_engine("sqlite:///./triage.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class TriageRecord(Base):
    __tablename__ = "triage_records"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = Column(String)
    chief_complaint = Column(Text)
    esi_level = Column(Integer)
    escalation = Column(String)
    confidence = Column(Float)
    agent_trace = Column(Text)
    correct_esi_level = Column(Integer, nullable=True)
    is_correct = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)