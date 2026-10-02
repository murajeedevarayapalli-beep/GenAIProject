import re
from typing import Any, Dict

from app.prompts.triage_prompt import TRIAGE_PROMPT


def triage_user_request(user_query: str, context: Dict[str, Any] | None = None) -> Dict[str, Any]:
    context = context or {}
    lowered = user_query.lower()

    order_match = re.search(r"ORD-[A-Z0-9-]+", user_query, re.IGNORECASE)
    customer_match = re.search(r"CUST-[A-Z0-9-]+", user_query, re.IGNORECASE)

    if "delay" in lowered or "late" in lowered or "not arrived" in lowered:
        intent = "delivery_delay"
        category = "delivery"
    elif "lost" in lowered or "missing" in lowered or "never arrived" in lowered:
        intent = "lost_package"
        category = "fulfillment"
    elif "refund" in lowered or "money back" in lowered:
        intent = "refund_request"
        category = "claims"
    else:
        intent = "general_support"
        category = "support"

    priority = "medium"
    if "urgent" in lowered or "asap" in lowered or "today" in lowered:
        priority = "high"

    entities = {
        "order_id": order_match.group(0).upper() if order_match else context.get("order_id"),
        "customer_id": customer_match.group(0).upper() if customer_match else context.get("customer_id"),
        "issue_keyword": intent,
    }

    missing = []
    if not entities.get("order_id"):
        missing.append("order_id")
    if not entities.get("customer_id"):
        missing.append("customer_id")

    return {
        "intent": intent,
        "category": category,
        "priority": priority,
        "entities": entities,
        "missing_information": missing,
        "confidence": 0.88 if not missing else 0.72,
        "recommended_route": "retrieval",
        "prompt": TRIAGE_PROMPT,
    }
