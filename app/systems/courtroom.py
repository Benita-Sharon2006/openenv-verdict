import random

def generate_courtroom_state(difficulty: str) -> dict:
    return {
        "judge_mood": random.uniform(0.5, 0.8),
        "jury_sentiment": random.uniform(0.3, 0.6),
        "opposing_counsel_strength": {"easy": 0.3, "medium": 0.6, "hard": 0.85}.get(difficulty, 0.6),
        "motions_filed": [],
        "objections_raised": [],
        "objections_sustained": 0,
        "objections_overruled": 0,
        "surprise_motions": _generate_surprise_motions(difficulty),
        "contempt_warnings": 0,
        "current_phase": "pre_trial",
    }

def _generate_surprise_motions(difficulty: str) -> list:
    all_motions = [
        {"id": "SM-001", "type": "suppress_evidence", "target": "EVD-001",
         "description": "Opposition moves to suppress CCTV footage", "handled": False},
        {"id": "SM-002", "type": "mistrial",
         "description": "Opposition claims juror misconduct", "handled": False},
        {"id": "SM-003", "type": "continuance",
         "description": "Opposition requests 30-day delay", "handled": False},
        {"id": "SM-004", "type": "dismiss",
         "description": "Opposition moves to dismiss for lack of evidence", "handled": False},
    ]
    counts = {"easy": 1, "medium": 2, "hard": 4}
    return all_motions[:counts.get(difficulty, 2)]

def file_motion(courtroom: dict, motion_type: str, argument: str) -> dict:
    courtroom["motions_filed"].append({"type": motion_type, "argument": argument})
    keywords = ["evidence", "witness", "precedent", "constitutional", "statute", "admissible"]
    hits = sum(1 for k in keywords if k in argument.lower())
    if hits >= 2 and len(argument) >= 30:
        courtroom["judge_mood"] = min(1.0, courtroom["judge_mood"] + 0.08)
        courtroom["jury_sentiment"] = min(1.0, courtroom["jury_sentiment"] + 0.05)
        return {"success": True, "message": f"Motion '{motion_type}' GRANTED. Judge impressed.", "reward": 0.12}
    else:
        courtroom["judge_mood"] = max(0.0, courtroom["judge_mood"] - 0.05)
        return {"success": True, "message": f"Motion '{motion_type}' DENIED. Weak argument.", "reward": 0.02}

def raise_objection(courtroom: dict, objection_type: str) -> dict:
    valid = ["hearsay", "relevance", "speculation", "leading", "badgering", "foundation"]
    if objection_type not in valid:
        return {"success": False, "message": f"Invalid objection. Valid: {valid}", "reward": -0.02}
    courtroom["objections_raised"].append(objection_type)
    if random.random() < courtroom["judge_mood"]:
        courtroom["objections_sustained"] += 1
        courtroom["jury_sentiment"] = min(1.0, courtroom["jury_sentiment"] + 0.04)
        return {"success": True, "message": f"Objection '{objection_type}' SUSTAINED.", "reward": 0.06}
    else:
        courtroom["objections_overruled"] += 1
        return {"success": True, "message": f"Objection '{objection_type}' OVERRULED.", "reward": 0.01}

def handle_surprise_motion(courtroom: dict, motion_id: str, counter_argument: str) -> dict:
    motion = next((m for m in courtroom["surprise_motions"] if m["id"] == motion_id), None)
    if not motion:
        return {"success": False, "message": f"Motion {motion_id} not found", "reward": -0.02}
    if motion["handled"]:
        return {"success": False, "message": "Already handled", "reward": -0.01}
    motion["handled"] = True
    keywords = ["evidence", "precedent", "rule", "statute", "court", "objection"]
    hits = sum(1 for k in keywords if k in counter_argument.lower())
    if hits >= 2 and len(counter_argument) >= 40:
        courtroom["judge_mood"] = min(1.0, courtroom["judge_mood"] + 0.1)
        return {"success": True, "message": f"Surprise motion {motion_id} defeated!", "reward": 0.15}
    else:
        courtroom["judge_mood"] = max(0.0, courtroom["judge_mood"] - 0.08)
        return {"success": True, "message": f"Failed to counter motion {motion_id}.", "reward": 0.02}

def get_courtroom_score(courtroom: dict) -> float:
    score = (courtroom["judge_mood"] * 0.4 + courtroom["jury_sentiment"] * 0.6)
    return round(min(0.99, max(0.01, score)), 4)