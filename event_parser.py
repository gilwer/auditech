from typing import Dict, Any

from models import NormalizedPullRequest


class WebhookEventParser:

    def paser_pull_request(self, event: Dict[str,Any]) -> NormalizedPullRequest:
        pr = event['pull_request']
        return NormalizedPullRequest.parse_obj(pr)