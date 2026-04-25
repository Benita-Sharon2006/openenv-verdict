"""VERDICT client — connects to HF Space or local server."""
from __future__ import annotations
from openenv.core import EnvClient
from models import VerdictAction, VerdictObservation

class VerdictEnv(EnvClient):
    """
    Remote client for the VERDICT legal war room environment.

    Usage (async):
        async with VerdictEnv(base_url="https://BenitaSharon-openenv-verdict.hf.space") as env:
            obs = await env.reset(difficulty="hard")
            result = await env.step(VerdictAction(action_type="inspect_all"))

    Usage (sync):
        with VerdictEnv(base_url="...").sync() as env:
            obs = env.reset()
    """
    action_type = VerdictAction
    observation_type = VerdictObservation