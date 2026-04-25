import time

def generate_cases(difficulty: str) -> list:
    all_cases = [
        {
            "id": "CASE-001",
            "title": "State v. Marcus Webb - Murder Trial",
            "type": "criminal",
            "priority": "critical",
            "client": "Marcus Webb",
            "status": "active",
            "deadline_seconds": 600,
            "created_at": time.time(),
            "filing_deadline": time.time() + 600,
            "strength": 0.3,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Client accused of first-degree murder. Key witness recanted. Need alibi evidence."
        },
        {
            "id": "CASE-002",
            "title": "TechCorp IP Theft - Civil Litigation",
            "type": "civil",
            "priority": "high",
            "client": "TechCorp Inc",
            "status": "active",
            "deadline_seconds": 800,
            "created_at": time.time(),
            "filing_deadline": time.time() + 800,
            "strength": 0.6,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Competitor stole proprietary algorithm. $50M in damages sought."
        },
        {
            "id": "CASE-003",
            "title": "Celebrity Divorce - Ramirez v. Ramirez",
            "type": "family",
            "priority": "high",
            "client": "Sofia Ramirez",
            "status": "active",
            "deadline_seconds": 900,
            "created_at": time.time(),
            "filing_deadline": time.time() + 900,
            "strength": 0.7,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "High-profile divorce. $200M estate. Hidden assets suspected."
        },
        {
            "id": "CASE-004",
            "title": "International Drug Cartel - Extradition",
            "type": "international",
            "priority": "critical",
            "client": "Colombian Government",
            "status": "active",
            "deadline_seconds": 400,
            "created_at": time.time(),
            "filing_deadline": time.time() + 400,
            "strength": 0.4,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Cross-border extradition treaty dispute. 3 jurisdictions involved."
        },
        {
            "id": "CASE-005",
            "title": "Corporate Fraud - Enfield Financial",
            "type": "white_collar",
            "priority": "high",
            "client": "SEC",
            "status": "active",
            "deadline_seconds": 700,
            "created_at": time.time(),
            "filing_deadline": time.time() + 700,
            "strength": 0.5,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Ponzi scheme defrauded 2,000 investors of $300M."
        },
        {
            "id": "CASE-006",
            "title": "Cybercrime - DarkNet Hacker Ring",
            "type": "cybercrime",
            "priority": "critical",
            "client": "FBI",
            "status": "active",
            "deadline_seconds": 350,
            "created_at": time.time(),
            "filing_deadline": time.time() + 350,
            "strength": 0.35,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "International hacker ring breached 50 banks. Digital evidence fragile."
        },
        {
            "id": "CASE-007",
            "title": "Medical Malpractice - Dr. Chen",
            "type": "civil",
            "priority": "medium",
            "client": "Patient Family",
            "status": "active",
            "deadline_seconds": 1000,
            "created_at": time.time(),
            "filing_deadline": time.time() + 1000,
            "strength": 0.65,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Surgical error caused permanent disability. Expert witness needed."
        },
        {
            "id": "CASE-008",
            "title": "Environmental Disaster - ChemCorp",
            "type": "environmental",
            "priority": "high",
            "client": "Local Community",
            "status": "active",
            "deadline_seconds": 750,
            "created_at": time.time(),
            "filing_deadline": time.time() + 750,
            "strength": 0.55,
            "assigned": False,
            "closed": False,
            "outcome": None,
            "description": "Chemical spill contaminated water supply of 100,000 residents."
        }
    ]
    if difficulty == "easy":
        return all_cases[:2]
    elif difficulty == "medium":
        return all_cases[:5]
    else:
        return all_cases

def get_cases_status(cases: list) -> dict:
    now = time.time()
    for case in cases:
        if not case["closed"]:
            remaining = case["filing_deadline"] - now
            case["deadline_remaining"] = max(0, int(remaining))
            case["expired"] = remaining <= 0
    return {
        "total": len(cases),
        "active": sum(1 for c in cases if not c["closed"]),
        "expired": sum(1 for c in cases if c.get("expired") and not c["closed"]),
        "closed": sum(1 for c in cases if c["closed"]),
        "cases": cases
    }

def assign_case(cases: list, case_id: str, priority: str) -> dict:
    case = next((c for c in cases if c["id"] == case_id), None)
    if not case:
        return {"success": False, "message": f"Case {case_id} not found", "reward": -0.02}
    if case["assigned"]:
        return {"success": False, "message": f"Case {case_id} already assigned", "reward": -0.01}
    case["assigned"] = True
    case["assigned_priority"] = priority
    reward = 0.05 if priority == case["priority"] else 0.02
    return {"success": True, "message": f"Case {case_id} assigned with priority {priority}", "reward": reward}

def close_case(cases: list, case_id: str, outcome: str) -> dict:
    case = next((c for c in cases if c["id"] == case_id), None)
    if not case:
        return {"success": False, "message": f"Case {case_id} not found", "reward": -0.02}
    if case["closed"]:
        return {"success": False, "message": "Already closed", "reward": -0.01}
    case["closed"] = True
    case["outcome"] = outcome
    if outcome == "won":
        return {"success": True, "message": f"Case {case_id} WON!", "reward": 0.15}
    elif outcome == "settled":
        return {"success": True, "message": f"Case {case_id} settled.", "reward": 0.08}
    else:
        return {"success": True, "message": f"Case {case_id} lost.", "reward": -0.05}

def get_case_score(cases: list) -> float:
    if not cases:
        return 0.5
    closed = [c for c in cases if c["closed"]]
    if not closed:
        return 0.01
    wins = sum(1 for c in closed if c.get("outcome") == "won")
    settlements = sum(1 for c in closed if c.get("outcome") == "settled")
    score = (wins * 1.0 + settlements * 0.5) / len(cases)
    return round(min(0.99, max(0.01, score)), 4)