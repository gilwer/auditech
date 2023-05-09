from typing import Dict, Any

import uvicorn
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from starlette import status

from models import NormalizedPullRequest
from repo import Repo, DetaRepo

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_repo():
    return DetaRepo()


@app.post("/pull-request", status_code=status.HTTP_200_OK)
async def handle_report(payload: Dict[str, Any], repo: Repo = Depends(get_repo)):
    pr = payload['pull_request']
    normalized_pr = NormalizedPullRequest.parse_obj(pr)
    repo.add_pull_request(normalized_pr)
    return {"message": "Pull request successfully stored"}


@app.get("/pull-request", status_code=status.HTTP_200_OK)
async def get_webhook_events(repo: Repo = Depends(get_repo)):
    return repo.get_pr()


@app.get("/", status_code=status.HTTP_200_OK)
async def health():
    return {'healthcheck': 'Everything OK!'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
