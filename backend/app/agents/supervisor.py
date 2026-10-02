from typing import Any, Dict


def supervise_workflow(state: Dict[str, Any]) -> Dict[str, Any]:
    intent = state.get("intent", {})
    missing = intent.get("missing_information", [])
    if missing:
        return {"supervisor_decision": {"next_agent": "triage", "reason": "More customer details are needed.", "requires_human_review": False}}

    return {"supervisor_decision": {"next_agent": "retrieval", "reason": "Order and policy evidence should be gathered.", "requires_human_review": False}}
