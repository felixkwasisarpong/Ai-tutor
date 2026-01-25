
from typing import Optional, Dict
from fastapi import UploadFile

def normalize_input(
        *,
        questions: Optional[str] = None,
        file: Optional[UploadFile] = None,

)->Dict:
        """
    Normalize any incoming user input into canonical text form.

    Returns:
    {
        "text": str,
        "input_type": str,
        "confidence": str,
    }
    """
        

        if questions and not file:
                return {
                        "text": questions,
                        "input_type": "text",
                        "confidence": "high",
                }

        if file:
                content_type = file.content_type or ""
                if content_type == "application/pdf":
                        return {
                                "text": "",
                                "input_type": "pdf",
                                "confidence": "medium",
                        }
                if content_type.startswith("image/"):
                        return {
                                "text": "",
                                "input_type": "image",
                                "confidence": "low",
                        }
                if content_type.startswith("audio/"):
                        return {
                                "text": "",
                                "input_type": "audio",
                                "confidence": "medium",
                        }
                raise ValueError(f"Unsupported file type: {content_type}")
        raise ValueError("No input provided")