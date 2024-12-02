# -*- coding: utf-8 -*-
# """
# development_code.py
# Created on Oct 21, 2024
# @ Author: Mazhar
# """

import os
from logging import Logger
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


def main() -> None:

    guard_agent = GuardAgent(
        number_of_messages_to_look_back=cfg.AGENTS.GUARD_AGENT.NUMBER_OF_MESSAGES_TO_LOOK_BACK
    )
    classification_agent = ClassificationAgent()
    recommendation_agent = RecommendationAgent(
        cfg.PATHS.APRIORI_RECOMMENDATIONS,
        cfg.PATHS.POPULARITY_RECOMMENDATIONS,
    )
    agent_dict: dict[str, AgentProtocol] = {
        "details_agent": DetailsAgent(),
        "recommendation_agent": recommendation_agent,
        "order_taking_agent": OrderTakingAgent(
            recommendation_agent, cfg.PATHS.MENU_ITEMS
        ),
    }

    messages: list = []
    while True:
        # Display the chat history
        os.system("cls" if os.name == "nt" else "clear")

        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")

        # Get user input
        prompt: str = input("User: ")
        messages.append({"role": "user", "content": prompt})

        # Get GuardAgent's response
        guard_agent_response: dict[str, Any] = guard_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            continue

        # Get ClassificationAgent's response
        classification_agent_response: dict[str, Any] = (
            classification_agent.get_response(messages)
        )
        chosen_agent: Any = classification_agent_response["memory"][
            "classification_decision"
        ]
        print("Chosen Agent: ", chosen_agent)

        # Get the chosen agent's response
        agent: AgentProtocol = agent_dict[chosen_agent]
        response: dict[str, Any] = agent.get_response(messages)

        messages.append(response)


if __name__ == "__main__":
    main()
