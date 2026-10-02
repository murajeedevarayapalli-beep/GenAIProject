from typing import Any, Dict, List

from app.tools.order_tools import get_customer_orders, get_order, get_tracking
from app.tools.policy_tools import search_policy_keywords


def retrieval_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    user_query = state.get("user_query", "")
    entities = state.get("intent", {}).get("entities", {})
    order_id = entities.get("order_id") or state.get("order_id")
    customer_id = entities.get("customer_id") or state.get("customer_id")

    retrieved_data: Dict[str, Any] = {}
    missing: List[str] = []

    if order_id:
        try:
            retrieved_data["order"] = get_order(order_id)
            retrieved_data["tracking"] = get_tracking(order_id)
        except ValueError:
            missing.append("order_id")
    else:
        missing.append("order_id")

    if customer_id:
        retrieved_data["customer_orders"] = get_customer_orders(customer_id)

    policy_matches = search_policy_keywords(user_query)
    retrieved_documents = [
        {
            "title": item["title"],
            "source": item["source"],
            "section": item["section"],
            "category": item["category"],
            "excerpt": item["text"],
        }
        for item in policy_matches
    ]

    return {
        "retrieved_data": retrieved_data,
        "retrieved_documents": retrieved_documents,
        "missing_information": missing,
    }
