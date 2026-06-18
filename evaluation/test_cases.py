TEST_CASES = [
    # ESI 1 — Immediate, life-threatening
    {
        "patient_id": "EVAL-001",
        "chief_complaint": "Found unresponsive at home",
        "symptoms": "Not breathing, no pulse detected by family member",
        "history": "Unknown",
        "vitals": "Unable to obtain",
        "correct_esi": 1,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-002",
        "chief_complaint": "Severe allergic reaction",
        "symptoms": "Swelling of face and throat, difficulty breathing, widespread hives",
        "history": "Known peanut allergy",
        "vitals": "BP 80/50, HR 130, SpO2 88%",
        "correct_esi": 1,
        "correct_escalation": "urgent"
    },

    # ESI 2 — High risk, severe distress
    {
        "patient_id": "EVAL-003",
        "chief_complaint": "Chest pain for 2 hours",
        "symptoms": "Shortness of breath, sweating, pain radiating to left arm",
        "history": "History of high blood pressure and diabetes",
        "vitals": "BP 160/95, HR 110",
        "correct_esi": 2,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-004",
        "chief_complaint": "Sudden severe headache",
        "symptoms": "Worst headache of life, neck stiffness, sensitivity to light",
        "history": "No prior history of migraines",
        "vitals": "BP 170/100, HR 95",
        "correct_esi": 2,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-005",
        "chief_complaint": "Severe abdominal pain",
        "symptoms": "Sudden onset, rigid abdomen, unable to stand straight",
        "history": "No prior surgeries",
        "vitals": "BP 100/70, HR 120, Temp 101.5F",
        "correct_esi": 2,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-006",
        "chief_complaint": "Suicidal ideation with a plan",
        "symptoms": "Expressing intent to harm self, has access to means",
        "history": "Diagnosed depression",
        "vitals": "BP 130/85, HR 90",
        "correct_esi": 2,
        "correct_escalation": "urgent"
    },

    # ESI 3 — Urgent, needs multiple resources
    {
        "patient_id": "EVAL-007",
        "chief_complaint": "Moderate abdominal pain for 6 hours",
        "symptoms": "Nausea, no vomiting, pain in lower right quadrant",
        "history": "No prior abdominal surgeries",
        "vitals": "BP 125/80, HR 88, Temp 100.2F",
        "correct_esi": 3,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-008",
        "chief_complaint": "Fall with possible wrist fracture",
        "symptoms": "Swelling and deformity of right wrist, moderate pain",
        "history": "No significant history",
        "vitals": "BP 128/82, HR 84",
        "correct_esi": 3,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-009",
        "chief_complaint": "Persistent vomiting and diarrhea for 2 days",
        "symptoms": "Unable to keep fluids down, feeling dizzy when standing",
        "history": "No significant history",
        "vitals": "BP 100/65, HR 105",
        "correct_esi": 3,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-010",
        "chief_complaint": "Moderate asthma exacerbation",
        "symptoms": "Wheezing, mild shortness of breath, responds partially to home inhaler",
        "history": "Known asthma",
        "vitals": "BP 120/78, HR 98, SpO2 94%",
        "correct_esi": 3,
        "correct_escalation": "urgent"
    },

    # ESI 4 — Less urgent, one resource
    {
        "patient_id": "EVAL-011",
        "chief_complaint": "Minor laceration on forearm",
        "symptoms": "Clean cut, bleeding controlled with pressure, no numbness",
        "history": "No significant history",
        "vitals": "BP 118/76, HR 72",
        "correct_esi": 4,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-012",
        "chief_complaint": "Twisted ankle while walking",
        "symptoms": "Mild swelling, able to bear some weight",
        "history": "No prior ankle injuries",
        "vitals": "BP 122/78, HR 76",
        "correct_esi": 4,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-013",
        "chief_complaint": "Urinary tract infection symptoms",
        "symptoms": "Burning with urination, mild lower abdominal discomfort",
        "history": "Prior UTIs in the past",
        "vitals": "BP 118/74, HR 80, Temp 99.1F",
        "correct_esi": 4,
        "correct_escalation": "routine"
    },

    # ESI 5 — Non-urgent, minimal resources
    {
        "patient_id": "EVAL-014",
        "chief_complaint": "Sore throat and mild fever for 2 days",
        "symptoms": "Mild cough, no shortness of breath",
        "history": "No significant medical history",
        "vitals": "Temp 99.8F, HR 78",
        "correct_esi": 5,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-015",
        "chief_complaint": "Requesting prescription refill",
        "symptoms": "No new symptoms, ran out of blood pressure medication",
        "history": "Controlled hypertension",
        "vitals": "BP 130/82, HR 74",
        "correct_esi": 5,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-016",
        "chief_complaint": "Mild seasonal allergy symptoms",
        "symptoms": "Sneezing, runny nose, itchy eyes",
        "history": "Known seasonal allergies",
        "vitals": "BP 120/76, HR 70",
        "correct_esi": 5,
        "correct_escalation": "routine"
    },

    # Ambiguous / needs more info cases
    {
        "patient_id": "EVAL-017",
        "chief_complaint": "Not feeling well",
        "symptoms": "Tired",
        "history": "Unknown",
        "vitals": "Not recorded",
        "correct_esi": None,
        "correct_escalation": "needs_more_info"
    },
    {
        "patient_id": "EVAL-018",
        "chief_complaint": "Pain",
        "symptoms": "Hurts somewhere",
        "history": "Unknown",
        "vitals": "Not recorded",
        "correct_esi": None,
        "correct_escalation": "needs_more_info"
    },

    # More mixed-severity cases for breadth
    {
        "patient_id": "EVAL-019",
        "chief_complaint": "Difficulty breathing for 30 minutes",
        "symptoms": "Audible wheezing, using accessory muscles to breathe, blue lips",
        "history": "Severe COPD",
        "vitals": "BP 140/90, HR 125, SpO2 84%",
        "correct_esi": 1,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-020",
        "chief_complaint": "High fever in a 2-year-old",
        "symptoms": "Temp 104F, lethargic, not drinking fluids",
        "history": "No significant history",
        "vitals": "Temp 104F, HR 160",
        "correct_esi": 2,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-021",
        "chief_complaint": "Back pain after lifting heavy object",
        "symptoms": "Sharp pain in lower back, no numbness or tingling in legs",
        "history": "Prior episodes of similar back pain",
        "vitals": "BP 124/80, HR 78",
        "correct_esi": 4,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-022",
        "chief_complaint": "Eye redness and irritation",
        "symptoms": "Mild discharge, no vision changes, no pain",
        "history": "No significant history",
        "vitals": "BP 118/74, HR 72",
        "correct_esi": 5,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-023",
        "chief_complaint": "Possible stroke symptoms",
        "symptoms": "Sudden facial droop, slurred speech, weakness on one side",
        "history": "History of atrial fibrillation",
        "vitals": "BP 180/100, HR 100",
        "correct_esi": 1,
        "correct_escalation": "urgent"
    },
    {
        "patient_id": "EVAL-024",
        "chief_complaint": "Moderate burn on hand",
        "symptoms": "Second-degree burn, approximately 3 inches, from hot pan",
        "history": "No significant history",
        "vitals": "BP 122/78, HR 82",
        "correct_esi": 4,
        "correct_escalation": "routine"
    },
    {
        "patient_id": "EVAL-025",
        "chief_complaint": "Routine follow-up for diabetes management",
        "symptoms": "No acute symptoms, here for scheduled check",
        "history": "Type 2 diabetes, well controlled",
        "vitals": "BP 128/80, HR 76",
        "correct_esi": 5,
        "correct_escalation": "routine"
    },
]