from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.agents.action import execute_action
from app.agents.investigation import investigate_case
from app.agents.response import generate_response
from app.agents.retrieval import retrieval_agent
from app.agents.triage import triage_user_request
from app.agents.validator import validate_state
from app.config import get_settings
from app.db import get_session, get_workflow, save_session, save_workflow
from app.rag.chunking import TextChunker
from app.rag.embeddings import EmbeddingService
from app.rag.loaders import KnowledgeLoader
from app.rag.vector_store import VectorStore
from app.schemas import ApprovalRequest, ChatRequest, HealthResponse, WorkflowResponse

settings = get_settings()
app = FastAPI(title=settings.app_name, version="1.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()


@app.get("/api/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", app=settings.app_name, environment=settings.app_env)


@app.get("/api/metrics")
async def metrics() -> Dict[str, Any]:
    return {
        "status": "ok",
        "workflow_count": len(getattr(__import__("app.db"), "WORKFLOW_STORE")),
        "session_count": len(getattr(__import__("app.db"), "SESSION_STORE")),
        "retrieval_count": len(vector_store.documents),
    }


@app.post("/api/chat")
async def chat(request: ChatRequest) -> Dict[str, Any]:
    session_id = request.session_id or str(uuid4())
    workflow_id = str(uuid4())

    state: Dict[str, Any] = {
        "session_id": session_id,
        "user_id": request.user_id,
        "workflow_id": workflow_id,
        "user_query": request.message,
        "conversation_history": [request.message],
        "entities": {},
        "retrieved_data": {},
        "retrieved_documents": [],
        "tool_results": [],
        "errors": [],
        "human_approval": {},
    }

    try:
        intent = triage_user_request(request.message, request.context)
        state["intent"] = intent
        state["entities"] = intent.get("entities", {})
    except Exception as exc:  # pragma: no cover
        state["errors"].append(str(exc))

    try:
        retrieval = retrieval_agent(state)
        state["retrieved_data"] = retrieval.get("retrieved_data", {})
        state["retrieved_documents"] = retrieval.get("retrieved_documents", [])
    except Exception as exc:  # pragma: no cover
        state["errors"].append(str(exc))

    try:
        investigation = investigate_case(state)
        state["investigation_result"] = investigation.get("investigation_result", {})
        state["proposed_actions"] = investigation.get("proposed_actions", [])
    except Exception as exc:  # pragma: no cover
        state["errors"].append(str(exc))

    try:
        action_result = execute_action(state)
        state["tool_results"] = action_result.get("tool_results", [])
    except Exception as exc:  # pragma: no cover
        state["errors"].append(str(exc))

    try:
        validation = validate_state(state)
        state["validation_result"] = validation.get("validation_result", {})
    except Exception as exc:  # pragma: no cover
        state["errors"].append(str(exc))

    response = generate_response(state)
    state["final_response"] = response.get("final_response", "")
    state["confidence"] = response.get("confidence", 0.0)

    workflow_payload = {
        "workflow_id": workflow_id,
        "session_id": session_id,
        "status": "completed",
        "state": state,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    save_session(session_id, {"session_id": session_id, "messages": state["conversation_history"]})
    save_workflow(workflow_id, workflow_payload)

    return {
        "workflow_id": workflow_id,
        "session_id": session_id,
        "status": "completed",
        "final_response": state["final_response"],
        "confidence": state["confidence"],
        "sources": state.get("retrieved_documents", []),
        "human_review_required": state.get("investigation_result", {}).get("requires_human_review", False),
        "validation": state.get("validation_result", {}),
    }


@app.post("/api/agent/run")
async def agent_run(request: ChatRequest) -> Dict[str, Any]:
    return await chat(request)


@app.post("/api/documents/upload")
async def upload_document() -> Dict[str, Any]:
    return {"status": "accepted", "message": "Document uploaded to the intake queue."}


@app.post("/api/documents/ingest")
async def ingest_documents() -> Dict[str, Any]:
    loader = KnowledgeLoader("/workspaces/GenAIProject/data/knowledge_base")
    text_docs = loader.load_documents()
    chunker = TextChunker(chunk_size=300, overlap=50)
    embedding_service = EmbeddingService()

    docs: List[Dict[str, Any]] = []
    for index, text in enumerate(text_docs):
        chunks = chunker.chunk(text)
        embeddings = embedding_service.embed_batch(chunks)
        for chunk_index, chunk in enumerate(chunks):
            docs.append(
                {
                    "document_id": f"doc-{index + 1}-{chunk_index + 1}",
                    "content": chunk,
                    "embedding": embeddings[chunk_index],
                    "source": f"knowledge_{index + 1}.md",
                    "metadata": {"category": "policy", "section": str(chunk_index + 1)},
                }
            )

    vector_store.add_documents(docs)
    return {"status": "ok", "documents_ingested": len(docs), "collection": vector_store.collection_name}


@app.get("/api/sessions/{session_id}")
async def get_session_info(session_id: str) -> Dict[str, Any]:
    session = get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session


@app.get("/api/workflows/{workflow_id}")
async def get_workflow_info(workflow_id: str) -> Dict[str, Any]:
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@app.post("/api/approval/{workflow_id}")
async def process_approval(workflow_id: str, request: ApprovalRequest) -> Dict[str, Any]:
    workflow = get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    workflow["state"]["human_approval"] = {
        "approved": request.approved,
        "notes": request.notes,
        "status": "approved" if request.approved else "rejected",
    }
    workflow["status"] = "awaiting_response" if request.approved else "rejected"
    save_workflow(workflow_id, workflow)
    return workflow["state"]["human_approval"]


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
