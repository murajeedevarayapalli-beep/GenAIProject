from typing import Any, Dict


def validate_state(state: Dict[str, Any]) -> Dict[str, Any]:
    investigation = state.get("investigation_result", {})
    evidence = investigation.get("evidence", [])
    policy_reference = investigation.get("policy_reference", [])
    requires_human = investigation.get("requires_human_review", False)

    if not evidence:
        return {"validation_result": {"decision": "RETRY", "reasons": ["No evidence found."], "required_fields": ["order_id"]}}
    if not policy_reference:
        return {"validation_result": {"decision": "HUMAN_REVIEW", "reasons": ["No policy supports the recommendation."], "required_fields": ["policy_reference"]}}
    if requires_human:
        return {"validation_result": {"decision": "HUMAN_REVIEW", "reasons": ["Sensitive action requires approval."], "required_fields": ["approval"]}}
    return {"validation_result": {"decision": "PASS", "reasons": ["Grounded recommendation validated."], "required_fields": []}}
