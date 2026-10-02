from typing import Any, Dict


def generate_response(state: Dict[str, Any]) -> Dict[str, Any]:
    intent = state.get("intent", {})
    investigation = state.get("investigation_result", {})
    documents = state.get("retrieved_documents", [])
    tool_results = state.get("tool_results", [])

    known_facts = [
        f"Customer issue classified as {intent.get('intent', 'support_request')}",
        f"Priority: {intent.get('priority', 'medium')}",
    ]
    evidence = investigation.get("evidence", [])
    policy_refs = investigation.get("policy_reference", [])

    final_response = (
        "I reviewed the available order and policy evidence and found a grounded recommendation. "
        "The current status indicates a support case that needs follow-up."
    )

    if investigation.get("requires_human_review"):
        final_response += " A human review is required before executing sensitive actions."

    return {
        "final_response": final_response,
        "known_facts": known_facts,
        "retrieved_evidence": evidence,
        "recommended_next_steps": [
            "Review the order and carrier evidence.",
            "Confirm the policy reference before action.",
            "Escalate if the issue is high-risk.",
        ],
        "completed_actions": [item["tool"] for item in tool_results if item.get("status") == "SUCCESS"],
        "pending_approval": [item["tool"] for item in tool_results if item.get("status") == "PENDING_APPROVAL"],
        "sources": documents,
        "confidence": investigation.get("confidence", 0.0),
    }
