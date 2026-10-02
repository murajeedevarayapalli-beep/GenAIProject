from typing import Any, Dict, List


def investigate_case(state: Dict[str, Any]) -> Dict[str, Any]:
    intent = state.get("intent", {})
    orders = state.get("retrieved_data", {}).get("order")
    tracking = state.get("retrieved_data", {}).get("tracking")
    policies = state.get("retrieved_documents", [])

    issue_type = "delivery_delay"
    evidence: List[str] = []
    policy_reference: List[str] = []

    if orders:
        evidence.append(f"Order {orders.get('order_id')} is currently {orders.get('status')}.")
    if tracking:
        evidence.append(f"Carrier {tracking.get('carrier')} reports {tracking.get('status')} with expected delivery {tracking.get('expected_delivery')}.")
    if policies:
        for item in policies:
            policy_reference.append(f"{item['title']} ({item['section']})")

    if orders and orders.get("status") == "LOST":
        issue_type = "lost_package"
        recommended_action = "initiate lost package investigation and replacement review"
        requires_human_review = True
    elif orders and orders.get("status") in {"IN_TRANSIT", "DELAYED"}:
        issue_type = "delivery_delay"
        recommended_action = "send customer update and escalate after policy threshold"
        requires_human_review = False
    else:
        issue_type = "general_support"
        recommended_action = "review supporting evidence and provide status update"
        requires_human_review = False

    return {
        "investigation_result": {
            "issue_type": issue_type,
            "evidence": evidence,
            "policy_reference": policy_reference,
            "recommended_action": recommended_action,
            "confidence": 0.84,
            "requires_human_review": requires_human_review,
        },
        "proposed_actions": [{"action": recommended_action, "requires_approval": requires_human_review}],
    }
