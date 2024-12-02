# -*- coding: utf-8 -*-
# """
# order_taking_agent.py
# Created on Oct 21, 2024
# @ Author: Mazhar
# """

import csv
import json
import os
from copy import deepcopy
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

from .utils import double_check_json_output, get_chatbot_response

load_dotenv()


class OrderTakingAgent:
    def __init__(self, recommendation_agent, menu_path: str) -> None:
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        self.model_name: str | None = os.getenv("MODEL_NAME")

        self.recommendation_agent: Any = recommendation_agent
        self.menu_path: str = menu_path

    def load_menu(self) -> str:
        menu_items: list[str] = []
        with open(self.menu_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                menu_items.append(f"{row['item']} - ${row['price']}")
        return "\n".join(menu_items)

    def get_response(self, messages) -> dict[str, Any]:
        messages: Any = deepcopy(messages)
        menu: str = self.load_menu()  # Load menu items from CSV
        # print(menu)
        base_prompt: str = f"""
        You are a customer support Bot for a coffee shop called "Merry's way"

        here is the menu for this coffee shop.

        {menu}  # Use the loaded menu here

        Things to NOT DO:
        * DON't ask how to pay by cash or Card.
        * Don't tell the user to go to the counter
        * Don't tell the user to go to place to get the order

        You're task is as follows:
        1. Take the User's Order
        2. Validate that all their items are in the menu
        3. if an item is not in the menu let the user and repeat back the remaining valid order
        4. Ask them if they need anything else.
        5. If they do then repeat starting from step 3
        6. If they don't want anything else. Using the "order" object that is in the output. Make sure to hit all three points
            1. list down all the items and their prices
            2. calculate the total. 
            3. Thank the user for the order and close the conversation with no more questions
        """

        output_format = """
        The user message will contain a section called memory. This section will contain the following:
            "order"
            "step number"
            please utilize this information to determine the next step in the process.
            
            produce the following output without any additions, not a single letter outside of the structure bellow.
            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": Write down your critical thinking about what is the maximum task number the user is on write now. Then write down your critical thinking about the user input and it's relation to the coffee shop process. Then write down your thinking about how you should respond in the response parameter taking into consideration the Things to NOT DO section. and Focus on the things that you should not do. 
            "step number": Determine which task you are on based on the conversation.
            "order": this is going to be a list of jsons like so. [{"item":put the item name, "quanitity": put the number that the user wants from this item, "price":put the total price of the item }]
            "response": write the a response to the user
            }
        """

        system_prompt: str = base_prompt + output_format

        last_order_taking_status = ""
        asked_recommendation_before = False
        for message_index in range(len(messages) - 1, 0, -1):
            message: Any = messages[message_index]

            agent_name: Any = message.get("memory", {}).get("agent", "")
            if message["role"] == "assistant" and agent_name == "order_taking_agent":
                step_number: Any = message["memory"]["step number"]
                order: Any = message["memory"]["order"]
                asked_recommendation_before: Any = message["memory"][
                    "asked_recommendation_before"
                ]
                last_order_taking_status: str = f"""
                step number: {step_number}
                order: {order}
                """
                break

        messages[-1]["content"] = (
            last_order_taking_status + " \n " + messages[-1]["content"]
        )

        input_messages: list = [{"role": "system", "content": system_prompt}] + messages

        chatbot_output: Any = get_chatbot_response(
            self.client, self.model_name, input_messages
        )

        # double check json
        chatbot_output: Any = double_check_json_output(
            self.client, self.model_name, chatbot_output
        )

        output: dict[str, Any] = self.postprocess(
            chatbot_output, messages, asked_recommendation_before
        )

        return output

    def postprocess(
        self, output, messages, asked_recommendation_before
    ) -> dict[str, Any]:
        output: Any = json.loads(output)

        if type(output["order"]) == str:
            output["order"] = json.loads(output["order"])

        response: Any = output["response"]
        if not asked_recommendation_before and len(output["order"]) > 0:
            recommendation_output: Any = (
                self.recommendation_agent.get_recommendations_from_order(
                    messages, output["order"]
                )
            )
            response = recommendation_output["content"]
            asked_recommendation_before = True

        dict_output: dict[str, Any] = {
            "role": "assistant",
            "content": response,
            "memory": {
                "agent": "order_taking_agent",
                "step number": output["step number"],
                "order": output["order"],
                "asked_recommendation_before": asked_recommendation_before,
            },
        }

        return dict_output