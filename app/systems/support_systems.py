import random

def generate_support_state(difficulty: str) -> dict:
    return {
        "firm_reputation": 0.7,
        "client_trust": 0.75,
        "budget_remaining": {"easy": 100000, "medium": 75000, "hard": 50000}.get(difficulty, 75000),
        "media_sentiment": random.uniform(0.3, 0.6),
        "leads": _generate_leads(difficulty),
        "client_communications": [],
        "press_releases": [],
        "settlement_offers": _generate_settlements(difficulty),
        "appeals": [],
    }

def _generate_leads(difficulty: str) -> list:
    all_leads = [
        {"id": "LEAD-001", "case_id": "CASE-001",
         "description": "Alibi witness spotted on social media",
         "followed_up": False, "outcome": None},
        {"id": "LEAD-002", "case_id": "CASE-002",
         "description": "Former employee willing to testify",
         "followed_up": False, "outcome": None},
        {"id": "LEAD-003", "case_id": "CASE-005",
         "description": "Whistleblower has additional documents",
         "followed_up": False, "outcome": None},
        {"id": "LEAD-004", "case_id": "CASE-006",
         "description": "Dark web forum post links to defendant",
         "followed_up": False, "outcome": None},
    ]
    counts = {"easy": 1, "medium": 2, "hard": 4}
    return all_leads[:counts.get(difficulty, 2)]

def _generate_settlements(difficulty: str) -> list:
    if difficulty == "easy":
        return []
    return [
        {"id": "SET-001", "case_id": "CASE-002",
         "offered_amount": 15000000, "our_demand": 50000000,
         "status": "pending", "deadline_steps": 10},
        {"id": "SET-002", "case_id": "CASE-007",
         "offered_amount": 500000, "our_demand": 2000000,
         "status": "pending", "deadline_steps": 8},
    ]

def communicate_with_client(support: dict, client_id: str, message: str) -> dict:
    support["client_communications"].append({"client": client_id, "message": message})
    keywords = ["update", "progress", "strategy", "evidence", "witness", "court", "settlement"]
    hits = sum(1 for k in keywords if k in message.lower())
    if hits >= 2 and len(message) >= 30:
        support["client_trust"] = min(1.0, support["client_trust"] + 0.06)
        return {"success": True, "message": f"Client {client_id} satisfied. Trust: {support['client_trust']:.2f}", "reward": 0.07}
    else:
        support["client_trust"] = max(0.0, support["client_trust"] - 0.03)
        return {"success": True, "message": f"Client {client_id} underwhelmed. Trust: {support['client_trust']:.2f}", "reward": 0.01}

def follow_lead(support: dict, lead_id: str) -> dict:
    lead = next((l for l in support["leads"] if l["id"] == lead_id), None)
    if not lead:
        return {"success": False, "message": f"Lead {lead_id} not found", "reward": -0.02}
    if lead["followed_up"]:
        return {"success": False, "message": "Already followed up", "reward": -0.01}
    lead["followed_up"] = True
    if random.random() > 0.3:
        lead["outcome"] = "valuable"
        support["firm_reputation"] = min(1.0, support["firm_reputation"] + 0.05)
        return {"success": True, "message": f"Lead {lead_id} was valuable! New evidence found.", "reward": 0.12}
    else:
        lead["outcome"] = "dead_end"
        return {"success": True, "message": f"Lead {lead_id} was a dead end.", "reward": 0.02}

def handle_settlement(support: dict, settlement_id: str, accept: bool) -> dict:
    settlement = next((s for s in support["settlement_offers"] if s["id"] == settlement_id), None)
    if not settlement:
        return {"success": False, "message": f"Settlement {settlement_id} not found", "reward": -0.02}
    if settlement["status"] != "pending":
        return {"success": False, "message": "Settlement already resolved", "reward": -0.01}
    if accept:
        settlement["status"] = "accepted"
        ratio = settlement["offered_amount"] / settlement["our_demand"]
        reward = round(0.05 + ratio * 0.15, 3)
        return {"success": True, "message": f"Settlement accepted: ${settlement['offered_amount']:,}", "reward": reward}
    else:
        settlement["status"] = "rejected"
        return {"success": True, "message": "Settlement rejected. Going to trial.", "reward": 0.03}

def issue_press_release(support: dict, statement: str, channel: str) -> dict:
    support["press_releases"].append({"statement": statement, "channel": channel})
    keywords = ["justice", "evidence", "client", "truth", "court", "law", "verdict"]
    hits = sum(1 for k in keywords if k in statement.lower())
    if hits >= 2:
        support["media_sentiment"] = min(1.0, support["media_sentiment"] + 0.08)
        support["firm_reputation"] = min(1.0, support["firm_reputation"] + 0.04)
        return {"success": True, "message": f"Press release on {channel} well received. Media: {support['media_sentiment']:.2f}", "reward": 0.08}
    else:
        support["media_sentiment"] = max(0.0, support["media_sentiment"] - 0.05)
        return {"success": True, "message": "Press release fell flat.", "reward": 0.01}

def file_appeal(support: dict, case_id: str, grounds: str) -> dict:
    support["appeals"].append({"case_id": case_id, "grounds": grounds, "status": "filed"})
    if len(grounds) >= 40:
        return {"success": True, "message": f"Appeal filed for {case_id}. Strong grounds.", "reward": 0.10}
    return {"success": True, "message": f"Appeal filed for {case_id}. Weak grounds.", "reward": 0.04}

def get_support_score(support: dict) -> float:
    score = (support["firm_reputation"] * 0.4 +
             support["client_trust"] * 0.4 +
             support["media_sentiment"] * 0.2)
    return round(min(0.99, max(0.01, score)), 4)