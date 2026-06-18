import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluation.test_cases import TEST_CASES
from agents.crew import run_triage
from app.database import SessionLocal, TriageRecord
import re
import time
import json

def extract_esi_and_escalation(result_text: str):
    # Search the full text, not just the start — handles "ESI level: 4", "ESI level 5", "esi level of 3"
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

def run_with_retry(intake_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = run_triage(intake_text)
            return str(result)
        except Exception as e:
            if "rate_limit" in str(e).lower() and attempt < max_retries - 1:
                wait_time = 15 * (attempt + 1)
                print(f"  Rate limited — waiting {wait_time}s before retry {attempt+2}/{max_retries}...")
                time.sleep(wait_time)
            else:
                raise e
    raise Exception("Max retries exceeded")

def run_evaluation():
    db = SessionLocal()
    results = []
    correct_esi = 0
    correct_escalation = 0
    total = len(TEST_CASES)

    print(f"\nRunning evaluation on {total} test cases...\n")
    print("Note: pacing requests to stay under Groq free-tier rate limits (30 RPM).\n")

    for i, case in enumerate(TEST_CASES):
        print(f"[{i+1}/{total}] {case['patient_id']}: {case['chief_complaint'][:50]}...")

        intake_text = f"""
Chief complaint: {case['chief_complaint']}
Symptoms: {case['symptoms']}
History: {case['history']}
Vitals: {case['vitals']}
"""
        start = time.time()
        try:
            result_text = run_with_retry(intake_text)
        except Exception as e:
            print(f"  ERROR (skipped after retries): {e}")
            results.append({
                "patient_id": case["patient_id"],
                "predicted_esi": None,
                "correct_esi": case["correct_esi"],
                "esi_match": False,
                "predicted_escalation": "error",
                "correct_escalation": case["correct_escalation"],
                "escalation_match": False,
                "latency_seconds": None,
                "skipped": True
            })
            time.sleep(20)  # cool down before next case
            continue

        latency = round(time.time() - start, 2)
        predicted_esi, predicted_escalation = extract_esi_and_escalation(result_text)

        esi_match = (predicted_esi == case["correct_esi"])
        escalation_match = (predicted_escalation == case["correct_escalation"])

        if esi_match:
            correct_esi += 1
        if escalation_match:
            correct_escalation += 1

        print(f"  Predicted: ESI={predicted_esi}, Escalation={predicted_escalation} | "
              f"Correct: ESI={case['correct_esi']}, Escalation={case['correct_escalation']} | "
              f"Match: ESI={'✓' if esi_match else '✗'} Escalation={'✓' if escalation_match else '✗'} | "
              f"{latency}s")

        record = TriageRecord(
            patient_id=case["patient_id"],
            chief_complaint=case["chief_complaint"],
            esi_level=predicted_esi,
            escalation=predicted_escalation,
            confidence=0.0,
            agent_trace=result_text,
            correct_esi_level=case["correct_esi"],
            is_correct=int(esi_match and escalation_match)
        )
        db.add(record)
        results.append({
            "patient_id": case["patient_id"],
            "predicted_esi": predicted_esi,
            "correct_esi": case["correct_esi"],
            "esi_match": esi_match,
            "predicted_escalation": predicted_escalation,
            "correct_escalation": case["correct_escalation"],
            "escalation_match": escalation_match,
            "latency_seconds": latency,
            "skipped": False
        })

        # Pace requests — each case makes 4 LLM calls, so wait between cases
        print("  Pausing 20s to respect rate limits...\n")
        time.sleep(20)

    db.commit()
    db.close()

    completed = [r for r in results if not r.get("skipped")]
    n_completed = len(completed)

    esi_accuracy = round(correct_esi / n_completed, 4) if n_completed else 0
    escalation_accuracy = round(correct_escalation / n_completed, 4) if n_completed else 0
    skipped_count = total - n_completed

    print(f"\n{'='*60}")
    print(f"EVALUATION COMPLETE")
    print(f"Cases completed: {n_completed}/{total} ({skipped_count} skipped due to rate limits)")
    print(f"ESI Level Accuracy: {esi_accuracy*100:.1f}% ({correct_esi}/{n_completed})")
    print(f"Escalation Accuracy: {escalation_accuracy*100:.1f}% ({correct_escalation}/{n_completed})")
    print(f"{'='*60}\n")

    with open("evaluation/results.json", "w") as f:
        json.dump({
            "esi_accuracy": esi_accuracy,
            "escalation_accuracy": escalation_accuracy,
            "total_cases": total,
            "completed_cases": n_completed,
            "skipped_cases": skipped_count,
            "correct_esi": correct_esi,
            "correct_escalation": correct_escalation,
            "detailed_results": results
        }, f, indent=2)

    print("Detailed results saved to evaluation/results.json")
    return results

if __name__ == "__main__":
    run_evaluation()