# -*- coding: utf-8 -*-
# """
# guard_agent.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """

import json
import os
from copy import deepcopy
from typing import Any

import openai
from dotenv import load_dotenv
from openai import OpenAI

from .utils import get_chatbot_response

load_dotenv()


class GuardAgent:
    def __init__(self, number_of_messages_to_look_back: int = 5) -> None:
        # Debug prints
        api_key = os.getenv("OPENAI_API_KEY")
        base_url = os.getenv("BASE_URL")

        print("Debug environment variables:")
        print(f"API Key exists: {api_key is not None}")
        print(f"API Key length: {len(api_key) if api_key else 0}")
        print(f"Base URL: {base_url}")

        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )

        # try:
        # # Initialize with minimal configuration
        #     self.client = OpenAI(
        #         api_key=api_key,
        #         base_url=base_url,
        #         timeout=20.0,  # explicit timeout
        #         max_retries=2  # explicit retries
        #     )
        # except Exception as e:
        #     print(f"Error initializing OpenAI client: {str(e)}")
        #     print(f"OpenAI package version: {openai.__version__}")  # Add this line
        #     raise

        self.model_name: str | None = os.getenv("MODEL_NAME")
        self.number_of_messages_to_look_back: int = number_of_messages_to_look_back

    def get_response(self, messages) -> dict[str, Any]:
        messages: Any = deepcopy(messages)

        system_prompt = """
            You are a helpful AI assistant for a coffee shop application which serves drinks and pastries.
            Your task is to determine whether the user is asking something relevant to the coffee shop or not.
            The user is allowed to:
            1. Ask questions about the coffee shop, like location, working hours, menue items and coffee shop related questions.
            2. Ask questions about menue items, they can ask for ingredients in an item and more details about the item.
            3. Make an order.
            4. Ask about recommendations of what to buy.
            5. If User greets you, you can greet them back.

            The user is NOT allowed to:
            1. Ask questions about anything else other than our coffee shop.
            2. Ask questions about the staff or how to make a certain menue item.

            Your output should be in a structured json format like so. each key is a string and each value is a string. Make sure to follow the format exactly:
            {
            "chain of thought": go over each of the points above and make see if the message lies under this point or not. Then you write some your thoughts about what point is this input relevant to.
            "decision": "allowed" or "not allowed". Pick one of those. and only write the word.
            "message": leave the message empty if it's allowed, otherwise write "Sorry, I can't help with that. Can I help you with your order?"
            }
            """

        input_messages: Any = [{"role": "system", "content": system_prompt}] + messages[
            -self.number_of_messages_to_look_back :
        ]
        # input_messages: Any = [{"role": "system", "content": system_prompt}] + messages[
        #     -3:
        # ]

        chatbot_output: Any = get_chatbot_response(
            self.client, self.model_name, input_messages
        )
        output: dict[str, Any] = self.postprocess(chatbot_output)

        return output

    def postprocess(self, output) -> dict[str, Any]:
        output: Any = json.loads(output)

        dict_output: dict[str, Any] = {
            "role": "assistant",
            "content": output["message"],
            "memory": {"agent": "guard_agent", "guard_decision": output["decision"]},
        }
        return dict_output
