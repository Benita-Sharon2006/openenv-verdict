import random

def generate_advanced_state(difficulty: str) -> dict:
    return {
        "forensics_lab": _generate_forensics(difficulty),
        "jury_selection": _generate_jury(difficulty),
        "cross_examinations": _generate_cross_exams(difficulty),
        "legal_research": [],
        "expert_consultations": [],
    }

def _generate_forensics(difficulty: str) -> list:
    all_samples = [
        {"id": "FOR-001", "case_id": "CASE-001", "type": "dna",
         "description": "Blood sample from crime scene",
         "tested": False, "result": None},
        {"id": "FOR-002", "case_id": "CASE-006", "type": "digital_forensics",
         "description": "Hard drive from suspected hacker",
         "tested": False, "result": None},
        {"id": "FOR-003", "case_id": "CASE-008", "type": "chemical",
         "description": "Water sample from contaminated area",
         "tested": False, "result": None},
    ]
    counts = {"easy": 1, "medium": 2, "hard": 3}
    return all_samples[:counts.get(difficulty, 2)]

def _generate_jury(difficulty: str) -> dict:
    return {
        "selected": False,
        "composition": [],
        "bias_detected": difficulty == "hard",
        "challenges_used": 0,
        "max_challenges": 6,
        "favorability": 0.5,
    }

def _generate_cross_exams(difficulty: str) -> list:
    if difficulty == "easy":
        return []
    return [
        {"id": "CX-001", "witness": "Prosecution Expert",
         "case_id": "CASE-001", "completed": False, "effectiveness": 0.0},
        {"id": "CX-002", "witness": "Opposing CFO",
         "case_id": "CASE-005", "completed": False, "effectiveness": 0.0},
    ]

def run_forensic_test(advanced: dict, sample_id: str, test_type: str) -> dict:
    sample = next((s for s in advanced["forensics_lab"] if s["id"] == sample_id), None)
    if not sample:
        return {"success": False, "message": f"Sample {sample_id} not found", "reward": -0.02}
    if sample["tested"]:
        return {"success": False, "message": "Already tested", "reward": -0.01}
    sample["tested"] = True
    if random.random() > 0.4:
        sample["result"] = "incriminating" if random.random() > 0.5 else "exculpatory"
        return {"success": True, "message": f"Forensic {test_type} on {sample_id}: {sample['result']}.", "reward": 0.12}
    else:
        sample["result"] = "inconclusive"
        return {"success": True, "message": f"Test inconclusive for {sample_id}.", "reward": 0.04}

def conduct_cross_examination(advanced: dict, cx_id: str, strategy: str) -> dict:
    cx = next((c for c in advanced["cross_examinations"] if c["id"] == cx_id), None)
    if not cx:
        return {"success": False, "message": f"Cross-exam {cx_id} not found", "reward": -0.02}
    if cx["completed"]:
        return {"success": False, "message": "Already completed", "reward": -0.01}
    cx["completed"] = True
    keywords = ["contradiction", "inconsistency", "prior statement",
                "evidence", "record", "fabricated"]
    hits = sum(1 for k in keywords if k in strategy.lower())
    effectiveness = min(1.0, hits * 0.15 + 0.1)
    cx["effectiveness"] = effectiveness
    return {"success": True,
            "message": f"Cross-exam {cx_id} done. Effectiveness: {effectiveness:.2f}",
            "reward": round(effectiveness * 0.15, 3)}

def conduct_legal_research(advanced: dict, topic: str) -> dict:
    advanced["legal_research"].append({"topic": topic, "completed": True})
    if len(topic) >= 20:
        return {"success": True,
                "message": f"Research on '{topic}' found strong precedent.",
                "reward": 0.08}
    return {"success": True,
            "message": f"Research on '{topic}' found limited precedent.",
            "reward": 0.03}

def consult_expert(advanced: dict, case_id: str, note: str) -> dict:
    advanced["expert_consultations"].append({"case_id": case_id, "note": note})
    if len(note) >= 30:
        return {"success": True,
                "message": f"Expert consultation for {case_id} successful.",
                "reward": 0.09}
    return {"success": True,
            "message": f"Expert consultation brief — limited value.",
            "reward": 0.03}

def get_advanced_score(advanced: dict) -> float:
    total = len(advanced["forensics_lab"]) or 1
    tested = sum(1 for s in advanced["forensics_lab"] if s["tested"])
    cx_total = len(advanced["cross_examinations"]) or 1
    cx_done = sum(1 for c in advanced["cross_examinations"] if c["completed"])
    score = (tested / total * 0.5) + (cx_done / cx_total * 0.5)
    return round(min(0.99, max(0.01, score)), 4)