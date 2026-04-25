import random

def generate_witnesses(difficulty: str) -> list:
    all_witnesses = [
        {"id": "WIT-001", "case_id": "CASE-001", "name": "Dr. Patricia Hayes",
         "type": "expert", "role": "forensic_pathologist", "reliability": 0.9,
         "prepared": False, "protected": False, "testified": False,
         "threatened": True, "credibility": 0.9,
         "testimony": "Time of death inconsistent with prosecution timeline"},
        {"id": "WIT-002", "case_id": "CASE-001", "name": "James Kowalski",
         "type": "eyewitness", "role": "neighbor", "reliability": 0.6,
         "prepared": False, "protected": False, "testified": False,
         "threatened": False, "credibility": 0.6,
         "testimony": "Saw defendant leaving scene at 11pm"},
        {"id": "WIT-003", "case_id": "CASE-002", "name": "Dr. Alan Turing Jr.",
         "type": "expert", "role": "software_expert", "reliability": 0.95,
         "prepared": False, "protected": False, "testified": False,
         "threatened": False, "credibility": 0.95,
         "testimony": "Code structure identical to plaintiff's proprietary algorithm"},
        {"id": "WIT-004", "case_id": "CASE-003", "name": "Swiss Bank Manager",
         "type": "expert", "role": "financial_expert", "reliability": 0.85,
         "prepared": False, "protected": False, "testified": False,
         "threatened": True, "credibility": 0.85,
         "testimony": "Confirms offshore accounts belong to defendant"},
        {"id": "WIT-005", "case_id": "CASE-005", "name": "Former CFO Linda Park",
         "type": "whistleblower", "role": "insider", "reliability": 0.8,
         "prepared": False, "protected": False, "testified": False,
         "threatened": True, "credibility": 0.8,
         "testimony": "CEO knowingly signed fraudulent financial statements"},
        {"id": "WIT-006", "case_id": "CASE-007", "name": "Dr. Robert Mills",
         "type": "expert", "role": "medical_expert", "reliability": 0.92,
         "prepared": False, "protected": False, "testified": False,
         "threatened": False, "credibility": 0.92,
         "testimony": "Standard of care was clearly violated during surgery"},
    ]
    if difficulty == "easy":
        return all_witnesses[:2]
    elif difficulty == "medium":
        return all_witnesses[:4]
    return all_witnesses

def prepare_witness(witnesses: list, witness_id: str) -> dict:
    wit = next((w for w in witnesses if w["id"] == witness_id), None)
    if not wit:
        return {"success": False, "message": f"Witness {witness_id} not found", "reward": -0.02}
    if wit["prepared"]:
        return {"success": False, "message": "Already prepared", "reward": -0.01}
    if wit["threatened"] and not wit["protected"]:
        return {"success": False, "message": f"Cannot prepare {witness_id} — witness is threatened! Protect first.", "reward": -0.03}
    wit["prepared"] = True
    wit["credibility"] = min(1.0, wit["credibility"] + 0.1)
    return {"success": True, "message": f"Witness {wit['name']} prepared. Credibility: {wit['credibility']:.2f}", "reward": 0.08}

def protect_witness(witnesses: list, witness_id: str, protection_level: str) -> dict:
    wit = next((w for w in witnesses if w["id"] == witness_id), None)
    if not wit:
        return {"success": False, "message": f"Witness {witness_id} not found", "reward": -0.02}
    if wit["protected"]:
        return {"success": False, "message": "Already protected", "reward": -0.01}
    wit["protected"] = True
    bonus = {"high": 0.12, "medium": 0.08, "low": 0.04}.get(protection_level, 0.06)
    return {"success": True, "message": f"Witness {wit['name']} protected at {protection_level} level.", "reward": bonus}

def call_witness(witnesses: list, witness_id: str) -> dict:
    wit = next((w for w in witnesses if w["id"] == witness_id), None)
    if not wit:
        return {"success": False, "message": f"Witness {witness_id} not found", "reward": -0.02}
    if wit["testified"]:
        return {"success": False, "message": "Already testified", "reward": -0.01}
    if not wit["prepared"]:
        return {"success": True, "message": f"{wit['name']} testified unprepared — low impact.", "reward": 0.03}
    wit["testified"] = True
    reward = round(wit["credibility"] * 0.15, 3)
    return {"success": True, "message": f"{wit['name']} testified: '{wit['testimony']}'. Impact: {reward:.3f}", "reward": reward}

def get_witness_score(witnesses: list) -> float:
    if not witnesses:
        return 0.5
    prepared = [w for w in witnesses if w["prepared"] and w["testified"]]
    return round(min(0.99, max(0.01, len(prepared) / len(witnesses))), 4)