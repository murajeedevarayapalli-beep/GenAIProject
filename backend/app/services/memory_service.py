from __future__ import annotations

from typing import Any, Dict, List, Optional


class MemoryService:
    def __init__(self):
        self.session_store: Dict[str, List[Dict[str, str]]] = {}

    def append_message(self, session_id: str, role: str, content: str) -> None:
        self.session_store.setdefault(session_id, []).append({"role": role, "content": content})

    def get_history(self, session_id: str) -> List[Dict[str, str]]:
        return self.session_store.get(session_id, [])

    def reset_session(self, session_id: str) -> None:
        self.session_store[session_id] = []

    def get_summary(self, session_id: str) -> Optional[str]:
        messages = self.get_history(session_id)
        if not messages:
            return None
        return " | ".join(f"{m['role']}: {m['content']}" for m in messages[-6:])
