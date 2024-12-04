from typing import List

from phi.document.base import Document
from phi.document.chunking.base import ChunkingStrategy


class RecursiveChunking(ChunkingStrategy):
    def __init__(self, chunk_size: int = 5000, overlap: int = 0, **kwargs):
        super().__init__(**kwargs)
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: Document) -> List[Document]:
        """Recursively chunk text by finding natural break points"""
        if len(document.content) <= self.chunk_size:
            return [document]

        chunks: List[Document] = []
        start = 0
        chunk_meta_data = document.meta_data
        chunk_number = 1
        content = document.content

        while start < len(content):
            end = min(start + self.chunk_size, len(content))

            if end < len(content):
                for sep in ["\n", "."]:
                    last_sep = content[start:end].rfind(sep)
                    if last_sep != -1:
                        end = start + last_sep + 1
                        break

            chunk = content[start:end]
            meta_data = chunk_meta_data.copy()
            meta_data["chunk"] = chunk_number
            chunk_id = None
            if document.id:
                chunk_id = f"{document.id}_{chunk_number}"
            meta_data["chunk_size"] = len(chunk)
            chunks.append(Document(id=chunk_id, name=document.name, meta_data=meta_data, content=chunk))

            start = max(start, end - self.overlap)

        return chunks
