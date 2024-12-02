# -*- coding: utf-8 -*-
# """
# details_agent.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """

import os
from copy import deepcopy
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI
from pinecone import Pinecone
from pinecone.data.index import Index

from .utils import get_chatbot_response, get_embedding

# from pinecone import QueryResponse


load_dotenv()


class DetailsAgent:
    def __init__(self) -> None:
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        self.embedding_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("BASE_URL"),
        )
        self.model_name: str | None = os.getenv("MODEL_NAME")
        self.embedding_model: str | None = os.getenv("EMBEDDING_MODEL")
        self.pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        self.index_name: str | None = os.getenv("PINECONE_INDEX_NAME")

    def get_closest_results(
        self, index_name, input_embeddings, top_k=2
    ) -> dict[str, Any] | None:
        index: Index = self.pc.Index(index_name)

        results: dict[str, Any] | None = index.query(
            namespace="ns1",
            vector=input_embeddings,
            top_k=top_k,
            include_values=False,
            include_metadata=True,
        )

        return results

    def get_response(self, messages) -> dict[str, Any]:
        messages: Any = deepcopy(messages)

        user_message: Any = messages[-1]["content"]
        embedding: Any = get_embedding(
            self.embedding_client, self.embedding_model, user_message
        )[0]
        result: Any = self.get_closest_results(self.index_name, embedding)
        source_knowledge: str = "\n".join(
            [x["metadata"]["text"].strip() + "\n" for x in result["matches"]]
        )

        prompt: str = f"""
        Using the contexts below, answer the query.

        Contexts:
        {source_knowledge}

        Query: {user_message}
        """

        system_prompt = """ You are a customer support agent for a coffee shop called Merry's way. 
        You should answer every question as if you are waiter and provide the neccessary information 
        to the user regarding their orders """
        messages[-1]["content"] = prompt
        input_messages: Any = [{"role": "system", "content": system_prompt}] + messages[
            -3:
        ]

        chatbot_output: Any = get_chatbot_response(
            self.client, self.model_name, input_messages
        )
        output: dict[str, Any] = self.postprocess(chatbot_output)
        return output

    def postprocess(self, output) -> dict[str, Any]:
        output: dict[str, Any] = {
            "role": "assistant",
            "content": output,
            "memory": {"agent": "details_agent"},
        }
        return output
