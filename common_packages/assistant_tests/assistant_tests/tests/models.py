from typing import Union, Optional

# ruff: noqa: E501
from pydantic import BaseModel

from . import response_comparators
from . import turn_requests


class Turn(BaseModel):
    request_type: str = "text_request"  # or "success" or "text_request" or "error"
    request: Optional[Union[str, dict]] = None
    response: Optional[Union[str, dict]] = None
    text_requests: object = turn_requests.default_text_requests
    success_requests: object = turn_requests.default_success_requests
    error_requests: object = turn_requests.default_error_requests
    response_comparator: object = None
    aggregation: object = all
    telemetry: dict = {}


class TestCase(BaseModel):
    name: str
    turns: list[Turn]
    response_comparator: object = response_comparators.is_in_plan

    def __getitem__(self, key):
        return self.turns[key]
