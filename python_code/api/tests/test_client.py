# -*- coding: utf-8 -*-
# """
# test_client.py
# Created on Nov 27, 2024
# @ Author: Mazhar
# To Run: Either run with full path e.g. pytest <your_full_path>/test_client.py -v -s
# or cd into tests directory and run pytest test_client.py -v -s
# """

import json
import os
import sys

import requests

# Add the directory containing 'api' to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from rich import print
from rich.traceback import install
from schemas import Input, Message, Messages, Response

install(show_locals=False)


def test_order_taking() -> None:
    # Get the absolute path to the test_input.json file
    test_input_path: str = os.path.join(os.path.dirname(__file__), "test_input.json")

    with open(test_input_path, "r") as f:
        data: Input = json.load(f)

    # Make the request
    response: requests.Response = requests.post(
        "http://localhost:8000/order_taking", json=data
    )

    # Print the response for debugging
    print("\nRequest Data:", data)
    print("\nResponse Status Code:", response.status_code)
    print("\nResponse Body:", response.json())

    # Assert statements to verify the response
    assert response.status_code == 200
    assert response.json() is not None


# def test_api() -> None:
#     # Read the test input
#     # Get the absolute path to the test_input.json file
#     test_input_path: str = os.path.join(os.path.dirname(__file__), "test_input.json")
#     # print(f"Test input path: {test_input_path}")

#     with open(test_input_path, "r") as f:
#         data: Input = json.load(f)

#     # Make the request
#     try:
#         response: requests.Response = requests.post(
#             "http://localhost:8000/order_taking", json=data
#         )
#         response.raise_for_status()  # Raise an exception for bad status codes
#         print("Response:", response.json())
#     except requests.exceptions.RequestException as e:
#         print(f"Error making request: {e}")


# if __name__ == "__main__":
#     test_api()
