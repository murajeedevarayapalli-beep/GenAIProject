from __future__ import annotations

from typing import Any, Dict

# Light local demo storage for sessions and workflow state.
SESSION_STORE: Dict[str, Dict[str, Any]] = {}
WORKFLOW_STORE: Dict[str, Dict[str, Any]] = {}


def save_session(session_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    SESSION_STORE[session_id] = payload
    return payload


def get_session(session_id: str) -> Dict[str, Any] | None:
    return SESSION_STORE.get(session_id)


def save_workflow(workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    WORKFLOW_STORE[workflow_id] = payload
    return payload


def get_workflow(workflow_id: str) -> Dict[str, Any] | None:
    return WORKFLOW_STORE.get(workflow_id)
