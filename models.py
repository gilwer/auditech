from pydantic import BaseModel


class User(BaseModel):
    login: str
    id: int


class NormalizedPullRequest(BaseModel):
    url: str
    id: int
    html_url: str
    diff_url: str
    number: int
    state: str
    title: str
    body: str
    user: User
    created_at: str
    updated_at: str

