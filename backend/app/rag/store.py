import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os
from typing import List

STORE_DIR = "/app/rag_store"
INDEX_PATH = os.path.join(STORE_DIR, "index.faiss")
TEXTS_PATH = os.path.join(STORE_DIR, "texts.pkl")
META_PATH = os.path.join(STORE_DIR, "metadata.pkl")


class VectorStore:
    def __init__(self, dim: int = 384):
        os.makedirs(STORE_DIR, exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts: List[str] = []
        self.metadatas: List[dict] = []
        self._load_if_exists()

    def add(self, chunks, persist: bool = True):
        if not chunks:
            return

        if isinstance(chunks[0], str):
            texts = chunks
            metadatas = [{} for _ in chunks]
        else:
            texts = [c["text"] for c in chunks]
            metadatas = [c["metadata"] for c in chunks]

        embeddings = self.model.encode(texts)
        self.index.add(np.array(embeddings).astype("float32"))

        self.texts.extend(texts)
        self.metadatas.extend(metadatas)
        if persist:
            self._persist()

    def add_documents(self, chunks):
        self.add(chunks, persist=True)

    def search(self, query: str, k: int = 3, filters: dict | None = None):
        if self.index.ntotal == 0:
            return []

        q_emb = self.model.encode([query])
        search_k = self.index.ntotal if filters else k
        _, indices = self.index.search(
            np.array(q_emb).astype("float32"), min(search_k, self.index.ntotal)
        )

        results = []
        for i in indices[0]:
            if i < len(self.texts):
                results.append(
                    {
                        "text": self.texts[i],
                        "metadata": self.metadatas[i],
                    }
                )

        if not filters:
            return results

        filtered = []
        for item in results:
            metadata = item.get("metadata", {})
            if all(metadata.get(key) == value for key, value in filters.items()):
                filtered.append(item)

        return filtered[:k]
    
    def _persist(self):
        print(f"Persisting FAISS index to {INDEX_PATH}")
        faiss.write_index(self.index, INDEX_PATH)

        print(f"Persisting texts to {TEXTS_PATH}")
        with open(TEXTS_PATH, "wb") as f:
            pickle.dump(self.texts, f)

        print(f"Persisting metadata to {META_PATH}")
        with open(META_PATH, "wb") as f:
            pickle.dump(self.metadatas, f)

            
    def _load_if_exists(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(TEXTS_PATH) and os.path.exists(META_PATH):
            print("Found persisted RAG store on disk")
            self.index = faiss.read_index(INDEX_PATH)
            with open(TEXTS_PATH, "rb") as f:
                self.texts = pickle.load(f)
            with open(META_PATH, "rb") as f:
                self.metadatas = pickle.load(f)
            print(f"Loaded persisted FAISS index with {self.index.ntotal} vectors")

vector_store = VectorStore()
