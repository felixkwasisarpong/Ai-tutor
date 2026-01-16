import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


class VectorStore:
    def __init__(self, dim: int = 384):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []

    def add(self, chunks):
        embeddings = self.model.encode(chunks)
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(chunks)

    def search(self, query: str, k: int = 3):
        if len(self.texts) == 0:
            return []

        q_emb = self.model.encode([query])
        distances, indices = self.index.search(
            np.array(q_emb).astype("float32"), k
        )

        return [self.texts[i] for i in indices[0] if i < len(self.texts)]

vector_store = VectorStore()