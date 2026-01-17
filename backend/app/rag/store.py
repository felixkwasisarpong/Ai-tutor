import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import pickle
import os

STORE_DIR = "/app/rag_store"
INDEX_PATH = os.path.join(STORE_DIR, "index.faiss")
TEXTS_PATH = os.path.join(STORE_DIR, "texts.pkl")


class VectorStore:
    def __init__(self, dim: int = 384):
        os.makedirs(STORE_DIR, exist_ok=True)
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self._load_if_exists()

    def add(self, chunks, persist: bool = True):
        embeddings = self.model.encode(chunks)
        self.index.add(np.array(embeddings).astype("float32"))
        self.texts.extend(chunks)
        if persist:
            self._persist()

    def add_documents(self, chunks):
        self.add(chunks, persist=True)

    def search(self, query: str, k: int = 3):
        if len(self.texts) == 0:
            return []

        q_emb = self.model.encode([query])
        _, indices = self.index.search(np.array(q_emb).astype("float32"), k)


        return [self.texts[i] for i in indices[0] if i < len(self.texts)]
    
    def _persist(self):
        print(f"Persisting FAISS index to {INDEX_PATH}")
        faiss.write_index(self.index, INDEX_PATH)

        print(f"Persisting texts to {TEXTS_PATH}")
        with open(TEXTS_PATH, "wb") as f:
            pickle.dump(self.texts, f)

    def _load_if_exists(self):
        if os.path.exists(INDEX_PATH) and os.path.exists(TEXTS_PATH):
            print("Found persisted RAG store on disk")
            self.index = faiss.read_index(INDEX_PATH)
            with open(TEXTS_PATH, "rb") as f:
                self.texts = pickle.load(f)
            print(f"Loaded persisted FAISS index with {self.index.ntotal} vectors")

vector_store = VectorStore()
