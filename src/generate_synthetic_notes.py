import random
import pandas as pd
from datetime import datetime, timedelta

# Make results reproducible
random.seed(42)

NOTE_TYPES = ["nursing", "physician", "discharge"]
UNITS = ["ICU", "Ward", "ER"]

RISK_PHRASES = [
    "patient appears increasingly confused",
    "worsening shortness of breath",
    "family expresses concern about discharge readiness",
    "nurse reports escalating agitation overnight",
    "poor medication adherence reported",
    "declining mobility and increased fall risk",
    "persistent chest pain not relieved by medication",
    "signs of infection worsening"
]

STABLE_PHRASES = [
    "patient resting comfortably",
    "vital signs stable",
    "pain well controlled",
    "no acute distress",
    "tolerating diet well",
    "ambulating with assistance",
    "no new complaints"
]


def generate_note_text(risk_level):
    base = random.choice(STABLE_PHRASES)
    if risk_level > 0.5:
        risk = random.choice(RISK_PHRASES)
        return f"{base}. However, {risk}."
    return base


def generate_patient_notes(patient_id, num_notes=10):
    start_date = datetime.now() - timedelta(days=7)
    notes = []
    risk = 0.1

    for i in range(num_notes):
        timestamp = start_date + timedelta(hours=12 * i)
        risk = min(1.0, risk + random.uniform(0.0, 0.15))

        note = {
            "patient_id": patient_id,
            "timestamp": timestamp.isoformat(),
            "note_type": random.choice(NOTE_TYPES),
            "unit": random.choice(UNITS),
            "note_text": generate_note_text(risk),
            "risk_label": round(risk, 2)
        }
        notes.append(note)

    return notes


def generate_dataset(num_patients=200):
    all_notes = []

    for pid in range(1, num_patients + 1):
        num_notes = random.randint(5, 15)
        patient_notes = generate_patient_notes(pid, num_notes)
        all_notes.extend(patient_notes)

    return pd.DataFrame(all_notes)


if __name__ == "__main__":
    df = generate_dataset()
    df.to_csv("data/raw/synthetic_clinical_notes.csv", index=False)
    print("Synthetic dataset created at data/raw/synthetic_clinical_notes.csv")
