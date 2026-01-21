
from sqlalchemy.orm import Session
from app.db.models.document import Document


def next_document_version(
    db: Session,
    course_id,
    title: str,
    document_type: str,
) -> int:
    latest = (
        db.query(Document)
        .filter(
            Document.course_id == course_id,
            Document.title == title,
            Document.document_type == document_type,
        )
        .order_by(Document.version.desc())
        .first()
    )

    return 1 if not latest else latest.version + 1
