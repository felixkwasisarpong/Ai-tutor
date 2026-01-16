from app.rag.ingest import load_pdf, chunk_text
from app.rag.store import VectorStore

text = load_pdf("data/L3-knowledgebase.pdf")
chunks = chunk_text(text)

store = VectorStore()
store.add_documents(chunks)