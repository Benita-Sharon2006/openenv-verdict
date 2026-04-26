from pydantic import BaseModel
from typing import Optional, Dict, Any

class VerdictAction(BaseModel):
    action_type: str
    case_id: Optional[str] = None
    priority: Optional[str] = None
    evidence_id: Optional[str] = None
    decision: Optional[str] = None
    witness_id: Optional[str] = None
    protection_level: Optional[str] = None
    motion_type: Optional[str] = None
    motion_id: Optional[str] = None
    objection_type: Optional[str] = None
    argument: Optional[str] = None
    strategy: Optional[str] = None
    client_id: Optional[str] = None
    message: Optional[str] = None
    lead_id: Optional[str] = None
    statement: Optional[str] = None
    channel: Optional[str] = None
    settlement_id: Optional[str] = None
    accept: Optional[bool] = None
    grounds: Optional[str] = None
    sample_id: Optional[str] = None
    test_type: Optional[str] = None
    cx_id: Optional[str] = None
    topic: Optional[str] = None
    note: Optional[str] = None

class VerdictObservation(BaseModel):
    step: int = 0
    max_steps: int = 60
    difficulty: str = "medium"
    episode_id: str = ""
    reward: float = 0.0
    current_reward: float = 0.0
    cumulative_reward: float = 0.0
    last_action_result: str = ""
    done: bool = False
    cases_summary: Dict[str, Any] = {}
    evidence_summary: Dict[str, Any] = {}
    witness_summary: Dict[str, Any] = {}
    courtroom: Dict[str, Any] = {}
    firm: Dict[str, Any] = {}