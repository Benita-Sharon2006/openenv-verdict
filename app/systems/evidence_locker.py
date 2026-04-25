import random

def generate_evidence(difficulty: str) -> list:
    all_evidence = [
        {"id": "EVD-001", "case_id": "CASE-001", "type": "digital",
         "description": "CCTV footage from night of murder - possibly tampered",
         "admissible": None, "forged": True, "analyzed": False, "chain_of_custody": False, "strength": 0.0},
        {"id": "EVD-002", "case_id": "CASE-001", "type": "physical",
         "description": "Murder weapon with fingerprints - chain of custody broken",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": False, "strength": 0.0},
        {"id": "EVD-003", "case_id": "CASE-002", "type": "digital",
         "description": "Source code comparison showing 94% similarity",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": True, "strength": 0.0},
        {"id": "EVD-004", "case_id": "CASE-003", "type": "financial",
         "description": "Offshore bank records showing $50M hidden assets",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": True, "strength": 0.0},
        {"id": "EVD-005", "case_id": "CASE-004", "type": "digital",
         "description": "Encrypted communications between cartel leaders",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": False, "strength": 0.0},
        {"id": "EVD-006", "case_id": "CASE-005", "type": "financial",
         "description": "Ponzi scheme transaction records - 50,000 entries",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": True, "strength": 0.0},
        {"id": "EVD-007", "case_id": "CASE-006", "type": "digital",
         "description": "Malware source code traced to defendant IP address",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": False, "strength": 0.0},
        {"id": "EVD-008", "case_id": "CASE-007", "type": "medical",
         "description": "Surgical records showing deviation from standard of care",
         "admissible": None, "forged": False, "analyzed": False, "chain_of_custody": True, "strength": 0.0},
    ]
    if difficulty == "easy":
        return all_evidence[:2]
    elif difficulty == "medium":
        return all_evidence[:5]
    return all_evidence

def analyze_evidence(evidence_list: list, evidence_id: str) -> dict:
    evd = next((e for e in evidence_list if e["id"] == evidence_id), None)
    if not evd:
        return {"success": False, "message": f"Evidence {evidence_id} not found", "reward": -0.02}
    if evd["analyzed"]:
        return {"success": False, "message": "Already analyzed", "reward": -0.01}
    evd["analyzed"] = True
    if evd["forged"]:
        evd["admissible"] = False
        evd["strength"] = 0.0
        return {"success": True, "message": f"ALERT: {evidence_id} is FORGED!", "reward": 0.08}
    elif evd["chain_of_custody"]:
        evd["admissible"] = True
        evd["strength"] = round(random.uniform(0.6, 0.95), 2)
        return {"success": True, "message": f"{evidence_id} admissible. Strength: {evd['strength']}", "reward": 0.10}
    else:
        evd["admissible"] = False
        evd["strength"] = 0.0
        return {"success": True, "message": f"{evidence_id} inadmissible - broken chain of custody.", "reward": 0.05}

def fix_chain_of_custody(evidence_list: list, evidence_id: str) -> dict:
    evd = next((e for e in evidence_list if e["id"] == evidence_id), None)
    if not evd:
        return {"success": False, "message": f"Evidence {evidence_id} not found", "reward": -0.02}
    if evd["forged"]:
        return {"success": False, "message": "Cannot fix forged evidence", "reward": -0.05}
    evd["chain_of_custody"] = True
    if evd["analyzed"]:
        evd["admissible"] = True
        evd["strength"] = round(random.uniform(0.6, 0.95), 2)
    return {"success": True, "message": f"Chain of custody restored for {evidence_id}", "reward": 0.08}

def get_evidence_score(evidence_list: list) -> float:
    if not evidence_list:
        return 0.5
    analyzed = [e for e in evidence_list if e["analyzed"]]
    if not analyzed:
        return 0.01
    admissible = [e for e in analyzed if e["admissible"]]
    return round(min(0.99, max(0.01, len(admissible) / len(evidence_list))), 4)
