from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

from models import NormalizedPullRequest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()




class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    pull_requests = relationship("PullRequest", back_populates="user")



class PullRequest(Base):
    __tablename__ = "pull_requests"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String)
    html_url = Column(String)
    diff_url = Column(String)
    number = Column(Integer)
    state = Column(String)
    title = Column(String)
    body = Column(String)
    created_at = Column(String)
    updated_at = Column(String, index=True)
    user_id = Column(ForeignKey("user.id"))
    user = relationship("User", back_populates="pull_requests")

Base.metadata.create_all(bind=engine)
class Repo:

    def add_pull_request(self,normalized_pr: NormalizedPullRequest) -> None:
        session = SessionLocal()
        user = session.query(User).filter_by(login=normalized_pr.user.login).first()
        if not user:
            user = User(id=normalized_pr.id,login=normalized_pr.user.login)
            session.add(user)
            session.commit()
        session.merge(PullRequest(id=normalized_pr.id,
                                  url=normalized_pr.url,
                                  html_url=normalized_pr.html_url,
                                  diff_url=normalized_pr.diff_url,
                                  number=normalized_pr.number,
                                  state=normalized_pr.state,
                                  title=normalized_pr.title,
                                  body=normalized_pr.body,
                                  created_at=normalized_pr.created_at,
                                  updated_at=normalized_pr.updated_at,
                                  user_id=normalized_pr.id))

        session.commit()



    def get_pr(self) -> List[NormalizedPullRequest]:
        session = SessionLocal()
        events = session.query(PullRequest).all()
        return events