
from typing import Optional
from fastapi import UploadFile
from pypdf import PdfReader
from io import BytesIO


MAX_PAGES = 20


def extract_text_from_pdf(file: UploadFile) -> Optional[str]:
    if file.content_type != "application/pdf":
        return None

    raw = file.file.read()
    if not raw:
        return None
    reader = PdfReader(BytesIO(raw))

    text_parts = []

    for i, page in enumerate(reader.pages):
        if i >= MAX_PAGES:
            break
        page_text = page.extract_text()
        if page_text:
            text_parts.append(page_text)


    return "\n".join(text_parts).strip() or None
