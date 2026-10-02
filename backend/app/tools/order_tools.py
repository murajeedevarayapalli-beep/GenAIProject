from __future__ import annotations

from typing import Any, Dict


SAMPLE_ORDERS = {
    "ORD-1001": {
        "order_id": "ORD-1001",
        "customer_id": "CUST-1001",
        "status": "IN_TRANSIT",
        "carrier": "NorthStar Logistics",
        "tracking_number": "NS7654321",
        "expected_delivery": "2026-10-03",
        "destination": "Seattle, WA",
        "delivery_issue": "Delay at regional hub",
    },
    "ORD-1002": {
        "order_id": "ORD-1002",
        "customer_id": "CUST-1003",
        "status": "DELIVERED",
        "carrier": "RouteLy",
        "tracking_number": "RL987654",
        "expected_delivery": "2026-09-28",
        "destination": "Austin, TX",
        "delivery_issue": "No issue observed",
    },
    "ORD-1100": {
        "order_id": "ORD-1100",
        "customer_id": "CUST-1015",
        "status": "LOST",
        "carrier": "QuickMove",
        "tracking_number": "QM112233",
        "expected_delivery": "2026-10-02",
        "destination": "Miami, FL",
        "delivery_issue": "Package marked lost after transfer scan",
    },
}


def get_order(order_id: str) -> Dict[str, Any]:
    order = SAMPLE_ORDERS.get(order_id)
    if not order:
        raise ValueError(f"Order {order_id} not found.")
    return order


def get_customer_orders(customer_id: str) -> Dict[str, Any]:
    matches = [order for order in SAMPLE_ORDERS.values() if order["customer_id"] == customer_id]
    return {"customer_id": customer_id, "orders": matches}


def get_tracking(order_id: str) -> Dict[str, Any]:
    order = get_order(order_id)
    return {
        "tracking_number": order["tracking_number"],
        "carrier": order["carrier"],
        "status": order["status"],
        "expected_delivery": order["expected_delivery"],
    }
