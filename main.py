from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Request, Depends

from models import NormalizedPullRequest
from repo import PullRequest, SessionLocal, Repo

app = FastAPI()


def get_repo():
    return Repo()


# Endpoint to handle incoming webhook events
@app.post("/report")
async def handle_report(payload: Dict[str, Any], repo: Repo = Depends(get_repo)):
    pr = payload['pull_request']
    normalized_pr = NormalizedPullRequest.parse_obj(pr)
    repo.add_pull_request(normalized_pr)
    return {"message": "Webhook event stored in database"}


# Endpoint to retrieve stored webhook events
@app.get("/report")
async def get_webhook_events(repo: Repo = Depends(get_repo)):
    return repo.get_pr()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)
