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
    text: str | List[str],
    course_code: str,
    document: str,
    document_type: str | None = None,
    department: str | None = None,
    version: int | None = None,
    document_id: str | None = None,
    active: bool = True,
):
    chunks = text if isinstance(text, list) else chunk_text(text)
    normalized_course_code = course_code.upper()

    return [
        {
        "text": chunk,
        "metadata": {
            "course_code": normalized_course_code,
            "document": document,
            "document_type": document_type,
            "department": department,
            "version": version,
            "document_id": document_id,
            "active": active,
            "chunk_index": i,
        },
        }
        for i, chunk in enumerate(chunks)
    ]
