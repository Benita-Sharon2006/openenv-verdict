"""VERDICT server entry point."""
import os
from openenv.core.env_server.http_server import create_app
from server.verdict_environment import VerdictEnvironment

app = create_app(
    env_class=VerdictEnvironment,
    enable_web_interface=os.getenv("ENABLE_WEB_INTERFACE", "true").lower() == "true",
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)