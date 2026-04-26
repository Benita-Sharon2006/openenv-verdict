"""
VERDICT Environment — server-side implementation.
AI agent acts as lead attorney managing multiple simultaneous cases.
"""
from __future__ import annotations
import uuid
from typing import Any, Dict

from openenv.core import Environment
from openenv.core.client_types import StepResult

from app.systems.case_management import (
    generate_cases, get_cases_status, assign_case, close_case
)
from app.systems.evidence_locker import (
    generate_evidence, analyze_evidence, fix_chain_of_custody
)
from app.systems.witness_management import (
    generate_witnesses, prepare_witness, protect_witness, call_witness
)
from app.systems.courtroom import (
    generate_courtroom_state, file_motion, raise_objection, handle_surprise_motion
)
from app.systems.support_systems import (
    generate_support_state, communicate_with_client, follow_lead,
    handle_settlement, issue_press_release, file_appeal
)
from app.systems.advanced_systems import (
    generate_advanced_state, run_forensic_test,
    conduct_cross_examination, conduct_legal_research, consult_expert
)
from app.rewards.calculator import calculate_reward

DIFFICULTY_CONFIG = {
    "easy":   {"max_steps": 30},
    "medium": {"max_steps": 60},
    "hard":   {"max_steps": 100},
}

VALID_ACTIONS = {
    "inspect_all", "assign_case", "close_case",
    "analyze_evidence", "fix_chain_of_custody",
    "prepare_witness", "protect_witness", "call_witness",
    "file_motion", "raise_objection", "handle_surprise_motion",
    "communicate_client", "follow_lead", "handle_settlement",
    "issue_press_release", "file_appeal",
    "run_forensic_test", "conduct_cross_examination",
    "conduct_legal_research", "consult_expert",
    "no_op",
}


class VerdictEnvironment(Environment):

    def __init__(self):
        self._episode_id = ""
        self._step = 0
        self._difficulty = "medium"
        self._done = False
        self._cumulative_reward = 0.0
        self._last_result = "Episode not started. Call reset first."
        self._cases = []
        self._evidence = []
        self._witnesses = []
        self._courtroom = {}
        self._support = {}
        self._advanced = {}

    async def reset(self, **kwargs) -> Dict[str, Any]:
        difficulty = kwargs.get("difficulty", "medium")
        self._difficulty = difficulty if difficulty in DIFFICULTY_CONFIG else "medium"
        self._episode_id = str(uuid.uuid4())[:8]
        self._step = 0
        self._done = False
        self._cumulative_reward = 0.0

        self._cases = generate_cases(self._difficulty)
        self._evidence = generate_evidence(self._difficulty)
        self._witnesses = generate_witnesses(self._difficulty)
        self._courtroom = generate_courtroom_state(self._difficulty)
        self._support = generate_support_state(self._difficulty)
        self._advanced = generate_advanced_state(self._difficulty)

        self._last_result = (
            f"VERDICT episode {self._episode_id} [{self._difficulty.upper()}] started. "
            f"{len(self._cases)} active cases, {len(self._evidence)} evidence items, "
            f"{len(self._witnesses)} witnesses. Use inspect_all to see full status."
        )
        return self._build_observation()

    async def step(self, action: Dict[str, Any]) -> StepResult:
        if self._done:
            return StepResult(
                observation=self._build_observation(),
                reward=0.0, done=True,
                info={"error": "Episode done. Call reset()."}
            )

        self._step += 1
        action_type = action.get("action_type", "no_op")
        reward, msg = self._dispatch(action_type, action)
        self._last_result = msg
        self._cumulative_reward += reward

        cfg = DIFFICULTY_CONFIG[self._difficulty]
        self._done = self._step >= cfg["max_steps"]

        return StepResult(
            observation=self._build_observation(),
            reward=reward,
            done=self._done,
            info={}
        )

    @property
    def state(self) -> Dict[str, Any]:
        return {
            "observation": self._build_observation(),
            "done": self._done,
            "episode_id": self._episode_id,
            "cumulative_reward": self._cumulative_reward,
        }

    def _dispatch(self, action_type: str, action: Dict) -> tuple:
        if action_type not in VALID_ACTIONS:
            return -0.05, f"Unknown action '{action_type}'. Valid: {sorted(VALID_ACTIONS)}"

        a = action

        if action_type == "inspect_all":
            return self._inspect_all()
        elif action_type == "assign_case":
            r = assign_case(self._cases, a.get("case_id", ""), a.get("priority", "medium"))
            return r["reward"], r["message"]
        elif action_type == "close_case":
            r = close_case(self._cases, a.get("case_id", ""), a.get("decision", "won"))
            return r["reward"], r["message"]
        elif action_type == "analyze_evidence":
            r = analyze_evidence(self._evidence, a.get("evidence_id", ""))
            return r["reward"], r["message"]
        elif action_type == "fix_chain_of_custody":
            r = fix_chain_of_custody(self._evidence, a.get("evidence_id", ""))
            return r["reward"], r["message"]
        elif action_type == "prepare_witness":
            r = prepare_witness(self._witnesses, a.get("witness_id", ""))
            return r["reward"], r["message"]
        elif action_type == "protect_witness":
            r = protect_witness(self._witnesses, a.get("witness_id", ""),
                                a.get("protection_level", "medium"))
            return r["reward"], r["message"]
        elif action_type == "call_witness":
            r = call_witness(self._witnesses, a.get("witness_id", ""))
            return r["reward"], r["message"]
        elif action_type == "file_motion":
            r = file_motion(self._courtroom, a.get("motion_type", ""),
                            a.get("argument", ""))
            return r["reward"], r["message"]
        elif action_type == "raise_objection":
            r = raise_objection(self._courtroom, a.get("objection_type", ""))
            return r["reward"], r["message"]
        elif action_type == "handle_surprise_motion":
            r = handle_surprise_motion(self._courtroom, a.get("motion_id", ""),
                                       a.get("argument", ""))
            return r["reward"], r["message"]
        elif action_type == "communicate_client":
            r = communicate_with_client(self._support, a.get("client_id", ""),
                                        a.get("message", ""))
            return r["reward"], r["message"]
        elif action_type == "follow_lead":
            r = follow_lead(self._support, a.get("lead_id", ""))
            return r["reward"], r["message"]
        elif action_type == "handle_settlement":
            r = handle_settlement(self._support, a.get("settlement_id", ""),
                                  a.get("accept", False))
            return r["reward"], r["message"]
        elif action_type == "issue_press_release":
            r = issue_press_release(self._support, a.get("statement", ""),
                                    a.get("channel", "twitter"))
            return r["reward"], r["message"]
        elif action_type == "file_appeal":
            r = file_appeal(self._support, a.get("case_id", ""),
                            a.get("grounds", ""))
            return r["reward"], r["message"]
        elif action_type == "run_forensic_test":
            r = run_forensic_test(self._advanced, a.get("sample_id", ""),
                                  a.get("test_type", "dna"))
            return r["reward"], r["message"]
        elif action_type == "conduct_cross_examination":
            r = conduct_cross_examination(self._advanced, a.get("cx_id", ""),
                                          a.get("strategy", ""))
            return r["reward"], r["message"]
        elif action_type == "conduct_legal_research":
            r = conduct_legal_research(self._advanced, a.get("topic", ""))
            return r["reward"], r["message"]
        elif action_type == "consult_expert":
            r = consult_expert(self._advanced, a.get("case_id", ""),
                               a.get("note", ""))
            return r["reward"], r["message"]
        else:
            return -0.02, "no_op — time is passing, deadlines approaching."

    def _inspect_all(self) -> tuple:
        cases_status = get_cases_status(self._cases)
        unanalyzed = [e["id"] for e in self._evidence if not e["analyzed"]]
        unprepared = [w["id"] for w in self._witnesses if not w["prepared"]]
        threatened = [w["id"] for w in self._witnesses
                      if w["threatened"] and not w["protected"]]
        pending_settlements = [s["id"] for s in self._support.get("settlement_offers", [])
                               if s["status"] == "pending"]
        unhandled_motions = [m["id"] for m in self._courtroom.get("surprise_motions", [])
                             if not m["handled"]]

        msg = (
            f"VERDICT STATUS [Step {self._step}]:\n"
            f"  Cases      -> {cases_status['active']} active, "
            f"{cases_status['closed']} closed, {cases_status['expired']} expired\n"
            f"  Evidence   -> {len(unanalyzed)} unanalyzed: {unanalyzed}\n"
            f"  Witnesses  -> {len(unprepared)} unprepared: {unprepared}\n"
            f"  URGENT     -> {len(threatened)} threatened witnesses: {threatened}\n"
            f"  Courtroom  -> Judge: {self._courtroom['judge_mood']:.2f} "
            f"| Jury: {self._courtroom['jury_sentiment']:.2f}\n"
            f"  Motions    -> {len(unhandled_motions)} pending: {unhandled_motions}\n"
            f"  Settlements-> {len(pending_settlements)} pending: {pending_settlements}\n"
            f"  Firm       -> Reputation: {self._support['firm_reputation']:.2f} "
            f"| Trust: {self._support['client_trust']:.2f}"
        )
        return 0.02, msg

    def _build_observation(self) -> Dict[str, Any]:
        cfg = DIFFICULTY_CONFIG[self._difficulty]
        final_reward = calculate_reward(
            self._cases, self._evidence, self._witnesses,
            self._courtroom, self._support, self._advanced,
            self._step, cfg["max_steps"]
        )
        return {
            "step": self._step,
            "max_steps": cfg["max_steps"],
            "difficulty": self._difficulty,
            "episode_id": self._episode_id,
            "cases_summary": {
                "total": len(self._cases),
                "active": sum(1 for c in self._cases if not c["closed"]),
                "closed": sum(1 for c in self._cases if c["closed"]),
            },
            "evidence_summary": {
                "total": len(self._evidence),
                "analyzed": sum(1 for e in self._evidence if e["analyzed"]),
                "admissible": sum(1 for e in self._evidence if e.get("admissible")),
            },
            "witness_summary": {
                "total": len(self._witnesses),
                "prepared": sum(1 for w in self._witnesses if w["prepared"]),
                "threatened": sum(1 for w in self._witnesses
                                  if w["threatened"] and not w["protected"]),
            },
            "courtroom": {
                "judge_mood": self._courtroom["judge_mood"],
                "jury_sentiment": self._courtroom["jury_sentiment"],
                "surprise_motions_pending": sum(
                    1 for m in self._courtroom.get("surprise_motions", [])
                    if not m["handled"]
                ),
            },
            "firm": {
                "reputation": self._support["firm_reputation"],
                "client_trust": self._support["client_trust"],
                "media_sentiment": self._support["media_sentiment"],
            },
            "current_reward": final_reward,
            "cumulative_reward": round(self._cumulative_reward, 4),
            "last_action_result": self._last_result,
            "done": self._done,
        }