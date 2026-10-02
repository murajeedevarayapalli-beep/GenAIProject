from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class TriageOutput(BaseModel):
    intent: str
    category: str
    priority: str
    entities: Dict[str, Any] = Field(default_factory=dict)
    missing_information: List[str] = Field(default_factory=list)
    confidence: float = 0.0
    recommended_route: str


class ChatRequest(BaseModel):
    user_id: str = "guest-user"
    session_id: Optional[str] = None
    message: str
    context: Dict[str, Any] = Field(default_factory=dict)


class ApprovalRequest(BaseModel):
    approved: bool
    notes: Optional[str] = None


class AgentRun(BaseModel):
    workflow_id: str
    agent: str
    status: str
    latency_ms: int
    result: Dict[str, Any] = Field(default_factory=dict)


class WorkflowResponse(BaseModel):
    workflow_id: str
    session_id: str
    status: str
    final_response: str
    confidence: float = 0.0
    sources: List[Dict[str, Any]] = Field(default_factory=list)
    human_review_required: bool = False
    approval_status: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    app: str
    environment: str
