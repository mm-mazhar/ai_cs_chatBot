# -*- coding: utf-8 -*-
# """
# schema.py
# Created on Oct 21, 2024
# @ Author: Mazhar
# """

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel
from typing_extensions import TypedDict

# from typing import TypedDict


class Message(TypedDict):
    role: Literal["user", "assistant", "system"]
    content: str


class Messages(TypedDict):
    messages: List[Message]


class Input(TypedDict):
    input: Messages


class Memory(TypedDict, total=False):
    agent: str
    step_number: str
    order: List[Dict[str, Any]]
    asked_recommendation_before: bool


class OrderTakingResponse(BaseModel):
    role: str
    content: str
    memory: Optional[Memory]
