from typing import Any, Dict, List, TypedDict


class AgentState(TypedDict, total=False):
    session_id: str
    user_id: str
    workflow_id: str
    user_query: str
    conversation_history: List[str]
    intent: Dict[str, Any]
    entities: Dict[str, Any]
    retrieved_data: Dict[str, Any]
    retrieved_documents: List[Dict[str, Any]]
    investigation_result: Dict[str, Any]
    proposed_actions: List[Dict[str, Any]]
    tool_results: List[Dict[str, Any]]
    confidence: float
    validation_result: Dict[str, Any]
    human_approval: Dict[str, Any]
    errors: List[str]
    final_response: str
