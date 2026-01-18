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

def make_chunks(
    chunks: list[str],
    *,
    department: str,
    course_code: str,
    document: str,
):
    return [
        {
            "text": chunk,
            "metadata": {
                "department": department,
                "course_code": course_code,
                "document": document,
                "chunk_index": i,
            },
        }
    for i, chunk in enumerate(chunks)
    ]