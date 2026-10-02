from typing import Any, Dict

from app.agents.action import execute_action
from app.agents.investigation import investigate_case
from app.agents.response import generate_response
from app.agents.retrieval import retrieval_agent
from app.agents.supervisor import supervise_workflow
from app.agents.triage import triage_user_request
from app.agents.validator import validate_state


def triage_node(state: Dict[str, Any]) -> Dict[str, Any]:
    triage = triage_user_request(state.get("user_query", ""), state.get("entities", {}))
    state["intent"] = triage
    state["confidence"] = triage.get("confidence", 0.0)
    return state


def supervisor_node(state: Dict[str, Any]) -> Dict[str, Any]:
    decision = supervise_workflow(state)
    state["supervisor_decision"] = decision["supervisor_decision"]
    return state


def retrieval_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = retrieval_agent(state)
    state["retrieved_data"] = result.get("retrieved_data", {})
    state["retrieved_documents"] = result.get("retrieved_documents", [])
    state["missing_information"] = result.get("missing_information", [])
    return state


def investigation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = investigate_case(state)
    state["investigation_result"] = result.get("investigation_result", {})
    state["proposed_actions"] = result.get("proposed_actions", [])
    return state


def action_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = execute_action(state)
    state["tool_results"] = result.get("tool_results", [])
    return state


def validation_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = validate_state(state)
    state["validation_result"] = result.get("validation_result", {})
    return state


def response_node(state: Dict[str, Any]) -> Dict[str, Any]:
    result = generate_response(state)
    state["final_response"] = result.get("final_response", "")
    state["confidence"] = result.get("confidence", state.get("confidence", 0.0))
    return state


def decision_node(state: Dict[str, Any]) -> Dict[str, Any]:
    investigation = state.get("investigation_result", {})
    if investigation.get("requires_human_review"):
        state["decision"] = "human_review"
    elif state.get("validation_result", {}).get("decision") == "RETRY":
        state["decision"] = "retry"
    else:
        state["decision"] = "response"
    return state
