"""VERDICT server entry point."""
import os
from openenv.core.env_server import create_app
from server.verdict_environment import VerdictEnvironment
from models import VerdictAction, VerdictObservation

env = VerdictEnvironment()

app = create_app(env, VerdictAction, VerdictObservation)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)