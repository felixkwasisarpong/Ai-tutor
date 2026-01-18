from pypdf import PdfReader
from typing import List


def load_pdf(path: str) -> str:
    reader = PdfReader(path)
    return "\n".join(page.extract_text() or "" for page in reader.pages)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap

    return chunks

def make_chunks(texts, *, course: str, document: str):
    return [
        {
            "text": t,
            "metadata": {
                "course": course,
                "document": document,
            },
        }
        for t in texts
    ]