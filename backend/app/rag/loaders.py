from pathlib import Path
from typing import List


class KnowledgeLoader:
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)

    def load_documents(self) -> List[str]:
        if not self.base_path.exists():
            return []
        docs: List[str] = []
        for file in sorted(self.base_path.glob("*.md")):
            docs.append(file.read_text(encoding="utf-8"))
        return docs
