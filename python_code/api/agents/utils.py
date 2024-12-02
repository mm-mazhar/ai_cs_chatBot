# -*- coding: utf-8 -*-
# """
# utils.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# """

from typing import Any


def get_chatbot_response(client, model_name, messages, temperature=0) -> Any:
    input_messages: list = []
    for message in messages:
        input_messages.append({"role": message["role"], "content": message["content"]})

    response: Any = (
        client.chat.completions.create(
            model=model_name,
            messages=input_messages,
            temperature=temperature,
            top_p=0.8,
            max_tokens=2000,
        )
        .choices[0]
        .message.content
    )

    return response


def get_embedding(embedding_client, model_name, text_input) -> list:
    output: Any = embedding_client.embeddings.create(input=text_input, model=model_name)

    embedings: list = []
    for embedding_object in output.data:
        embedings.append(embedding_object.embedding)

    return embedings


def double_check_json_output(client, model_name, json_string) -> Any:
    prompt: str = f""" You will check this json string and correct any mistakes that will make it invalid. Then you will return the corrected json string. Nothing else. 
    If the Json is correct just return it.

    Do NOT return a single letter outside of the json string.

    {json_string}
    """

    messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]

    response: Any = get_chatbot_response(client, model_name, messages)

    return response
