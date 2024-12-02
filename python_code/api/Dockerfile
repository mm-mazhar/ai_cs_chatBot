# FROM python:3.8.6-slim
# FROM python:3.13
FROM python:3.13.0a4-slim
# FROM python:3.11.3-slim-buster

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY agents/ agents/
COPY configs/ configs/
COPY logs/ logs/
COPY other_objects/ other_objects/
COPY recommendation_objects/ recommendation_objects/
COPY routers/ routers/
COPY schemas/ schemas/
COPY static/ static/
COPY agent_controller.py agent_controller.py
COPY main.py main.py

# Testing Dockerfile # TO REMOVE AFTER TESTING
COPY tests/test_input.json test_input.json


ENTRYPOINT [ "python", "main.py"]
