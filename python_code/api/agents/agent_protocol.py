# -*- coding: utf-8 -*-
# """
# agent_protocol.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """

from typing import Any, Protocol


class AgentProtocol(Protocol):
    def get_response(self, messages: list[dict[str, Any]]) -> dict[str, Any]: ...
