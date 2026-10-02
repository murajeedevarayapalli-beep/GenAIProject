from typing import List


class TextChunker:
    def __init__(self, chunk_size: int = 300, overlap: int = 50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text: str) -> List[str]:
        if len(text) <= self.chunk_size:
            return [text]
        chunks: List[str] = []
        start = 0
        while start < len(text):
            end = min(len(text), start + self.chunk_size)
            chunk = text[start:end]
            chunks.append(chunk)
            start += self.chunk_size - self.overlap
        return chunks
