from typing import Any, Dict

try:
    from langgraph.graph import StateGraph
except ImportError:  # pragma: no cover
    StateGraph = None

from app.graph.edges import route_after_investigation, route_after_supervisor, route_after_validation
from app.graph.nodes import (
    action_node,
    decision_node,
    investigation_node,
    response_node,
    retrieval_node,
    supervisor_node,
    triage_node,
    validation_node,
)
from app.graph.state import AgentState


if StateGraph is not None:
    workflow = StateGraph(AgentState)
    workflow.add_node("triage", triage_node)
    workflow.add_node("supervisor", supervisor_node)
    workflow.add_node("retrieval", retrieval_node)
    workflow.add_node("investigation", investigation_node)
    workflow.add_node("action", action_node)
    workflow.add_node("validation", validation_node)
    workflow.add_node("response", response_node)
    workflow.add_node("decision", decision_node)

    workflow.set_entry_point("triage")
    workflow.add_edge("triage", "supervisor")
    workflow.add_conditional_edges("supervisor", route_after_supervisor, {"retrieval": "retrieval", "response": "response"})
    workflow.add_edge("retrieval", "investigation")
    workflow.add_conditional_edges("investigation", route_after_investigation, {"human_review": "response", "action": "action"})
    workflow.add_edge("action", "validation")
    workflow.add_conditional_edges("validation", route_after_validation, {"retrieval": "retrieval", "response": "response"})
    workflow.add_edge("response", "decision")
    workflow.set_finish_point("response")
else:
    workflow = None
