from abc import ABC, abstractmethod
from typing import List


from models import NormalizedPullRequest

from deta import Deta



class Repo(ABC):


    @abstractmethod
    def add_pull_request(self,normalized_pr: NormalizedPullRequest) -> None:
        pass


    @abstractmethod
    def get_pr(self) -> List[NormalizedPullRequest]:
        pass

class DetaRepo(Repo):
    def __init__(self):
        deta = Deta("a0mxnfza79r_Pn3GgsAxyZXW5zvV6bXurnmPGpw2ubvY")
        self.db = deta.Base("base")

    def add_pull_request(self,normalized_pr: NormalizedPullRequest) -> None:
        self.db.put(data=normalized_pr.json(),key=str(normalized_pr.id))



    def get_pr(self) -> List[NormalizedPullRequest]:
        events = self.db.fetch()
        return [NormalizedPullRequest.parse_raw(i["value"]) for i in events.items]