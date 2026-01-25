
from typing import Optional, Dict
from fastapi import UploadFile
from app.input.pdf import extract_text_from_pdf


def normalize_input(
    *,
    question: Optional[str] = None,
    file: Optional[UploadFile] = None,
) -> Dict[str, Optional[str]]:
    """
    Normalize incoming user input into canonical text form.
    """
    if question and not file:
        return {
            "question": question,
            "context_text": None,
            "modality": "text",
        }

    if file:
        content_type = file.content_type or ""
        if content_type == "application/pdf":
            pdf_text = extract_text_from_pdf(file)
            return {
                "question": question or "",
                "context_text": pdf_text or "",
                "modality": "pdf",
            }
        if content_type.startswith("image/"):
            return {
                "question": question or "",
                "context_text": "",
                "modality": "image",
            }
        if content_type.startswith("audio/"):
            return {
                "question": question or "",
                "context_text": "",
                "modality": "audio",
            }
        raise ValueError(f"Unsupported file type: {content_type}")

    raise ValueError("No input provided")
