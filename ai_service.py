import os

from openai import OpenAI

from schemas import (
    TicketClassification,
)

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

instructions = """
You are a support ticket classifier.

Determine:

- category
- priority
- assigned team
- short summary
- status

Allowed categories:
- incident
- request
- problem

Allowed priorities:
- low
- medium
- high
- critical

Allowed teams:
- platform-operations
- customer-support
- security
- networking
- database

Allowed statuses:
- open
- manual_review_required

A critical ticket must have status "manual_review_required".

Return only the requested structured data.
"""


def classify_ticket(message: str) -> TicketClassification:
    response = client.responses.create(
        model="gpt-4-turbo",
        instructions=instructions,
        input=message,
    )

    return TicketClassification.model_validate_json(response.output_text)
