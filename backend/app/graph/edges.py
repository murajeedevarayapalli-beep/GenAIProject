from typing import Any, Dict


def route_after_triage(state: Dict[str, Any]) -> str:
    intent = state.get("intent", {})
    if intent.get("missing_information"):
        return "needs_clarification"
    return "supervisor"


def route_after_supervisor(state: Dict[str, Any]) -> str:
    decision = state.get("supervisor_decision", {})
    if decision.get("next_agent") == "retrieval":
        return "retrieval"
    return "response"


def route_after_investigation(state: Dict[str, Any]) -> str:
    if state.get("investigation_result", {}).get("requires_human_review"):
        return "human_review"
    return "action"


def route_after_validation(state: Dict[str, Any]) -> str:
    decision = state.get("validation_result", {}).get("decision")
    if decision == "RETRY":
        return "retrieval"
    if decision == "BLOCK":
        return "response"
    return "response"
