from openai import OpenAI

from config import settings
from schemas import TicketClassification, TicketPriority, TicketStatus

client = OpenAI(api_key=settings.openai_api_key)

instructions = """
You are a support ticket classification system.

Your task is to analyze the provided support ticket and determine:
1. category
2. priority
3. assigned_team
4. summary
5. status

You MUST only use values from the allowed values listed below.

CATEGORY
- incident: An unexpected interruption, failure, outage, degradation, or malfunction
  of an existing service or system.
- request: The user is asking for something to be provided, changed, configured,
  enabled, disabled, or otherwise carried out.
- problem: An underlying or recurring issue that requires investigation to identify
  or eliminate its root cause.

PRIORITY
- low: Minor impact, little urgency, and no significant business impact.
- medium: Limited impact or a non-urgent issue affecting a user or small number
  of users.
- high: Significant impact, multiple users affected, or an issue requiring
  prompt attention.
- critical: Major production outage, widespread customer impact, severe business
  impact, serious security incident, or another situation requiring immediate
  attention.

ASSIGNED TEAM
You MUST select exactly one of:
- platform-operations
- customer-support
- security
- networking
- database

Choose the team that is best suited to resolve the issue based on the information
available in the ticket.

STATUS
- open: Normal ticket requiring action.
- manual_review_required: The ticket is critical and requires human review.

If priority is "critical", status MUST be "manual_review_required".
Otherwise, status MUST be "open".

SUMMARY
Create a short, factual summary of the ticket in one sentence.
Do not invent information that is not present in the ticket.

GENERAL RULES
- Use only information contained in the ticket.
- Do not invent facts, affected systems, teams, customers, or impact.
- If the ticket is ambiguous, make the best classification based on the available
  information.
- Always select exactly one value for category, priority, assigned_team, and status.
- Return the result using the provided structured output schema.
"""


def classify_ticket(message: str) -> TicketClassification:
    response = client.responses.create(
        model="gpt-4-turbo",
        instructions=instructions,
        input=message,
    )
    classification = TicketClassification.model_validate_json(response.output_text)

    # Enforce "manual_review_required"-flag, if the priority is critical!
    if classification.priority == TicketPriority.critical:
        classification.status = TicketStatus.manual_review_required
    else:
        classification.status = TicketStatus.open

    return classification
