from typing import Any, Dict, List


def execute_action(state: Dict[str, Any]) -> Dict[str, Any]:
    actions: List[Dict[str, Any]] = []
    for item in state.get("proposed_actions", []):
        action_name = item.get("action")
        if "refund" in action_name.lower() and item.get("requires_approval"):
            actions.append({"tool": "request_refund", "status": "PENDING_APPROVAL", "details": action_name})
        elif "replacement" in action_name.lower():
            actions.append({"tool": "create_replacement_request", "status": "SUCCESS", "details": action_name})
        else:
            actions.append({"tool": "create_ticket", "status": "SUCCESS", "details": action_name})

    return {"tool_results": actions}
