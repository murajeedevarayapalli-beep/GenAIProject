from __future__ import annotations

from typing import Any, Dict, List

POLICIES = [
    {
        "title": "Delivery Delay Policy",
        "source": "operations_policy_v3.pdf",
        "category": "delivery",
        "section": "3.2",
        "text": "If a shipment remains in transit over 48 hours past the expected delivery window, the case may be escalated and a customer update must be sent. Refunds require approval when the order value exceeds $100.",
    },
    {
        "title": "Lost Package Procedure",
        "source": "fulfillment_manual.md",
        "category": "claims",
        "section": "4.1",
        "text": "Lost packages require investigation with carrier confirmation, proof of last scan, and prior delivery state. Replacement requests are allowed when the carrier confirms loss.",
    },
    {
        "title": "Refund Approval Rule",
        "source": "finance_policy.md",
        "category": "refund",
        "section": "2.7",
        "text": "Refunds above $100 require human approval before final execution. Refunds under $100 may be auto-approved if the issue is supported by policy and evidence.",
    },
]


def search_policy_keywords(query: str) -> List[Dict[str, Any]]:
    query_lower = query.lower()
    matches = []
    for policy in POLICIES:
        if query_lower in policy["title"].lower() or query_lower in policy["text"].lower():
            matches.append(policy)
    return matches


def get_policy_by_category(category: str) -> List[Dict[str, Any]]:
    return [item for item in POLICIES if item["category"] == category]
