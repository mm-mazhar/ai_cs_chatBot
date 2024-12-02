# -*- coding: utf-8 -*-
# """
# agent_controller.py
# Created on Oct 21, 2024
# @ Author: Mazhar
# """

from typing import Any

from agents import (
    AgentProtocol,
    ClassificationAgent,
    DetailsAgent,
    GuardAgent,
    OrderTakingAgent,
    RecommendationAgent,
)
from configs import cfg
from rich import print
from rich.traceback import install

install(show_locals=False, width=120)


class AgentController:
    def __init__(self) -> None:
        self.guard_agent = GuardAgent()
        self.classification_agent = ClassificationAgent()
        self.recommendation_agent = RecommendationAgent(
            cfg.PATHS.APRIORI_RECOMMENDATIONS,
            cfg.PATHS.POPULARITY_RECOMMENDATIONS,
        )

        self.agent_dict: dict[str, AgentProtocol] = {
            "details_agent": DetailsAgent(),
            "recommendation_agent": self.recommendation_agent,
            "order_taking_agent": OrderTakingAgent(
                self.recommendation_agent, cfg.PATHS.MENU_ITEMS
            ),
        }

    def get_response(self, input) -> dict[str, Any]:
        # Extract User Input
        job_input: Any = input["input"]
        messages: Any = job_input["messages"]

        # Get GuardAgent's response
        guard_agent_response: dict[str, Any] = self.guard_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            return guard_agent_response

        # Get ClassificationAgent's response
        classification_agent_response: dict[str, Any] = (
            self.classification_agent.get_response(messages)
        )
        chosen_agent: Any = classification_agent_response["memory"][
            "classification_decision"
        ]

        # Get the chosen agent's response
        agent: AgentProtocol = self.agent_dict[chosen_agent]
        response: dict[str, Any] = agent.get_response(messages)

        return response
