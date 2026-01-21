import uuid
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base
from sqlalchemy import func

from sqlalchemy.orm import relationship

class Document(Base):
    __tablename__ = "documents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    document_type: Mapped[str] = mapped_column(
        String, nullable=False
    )  # lecture, assignment, notes, etc.

    version: Mapped[int] = mapped_column(
        Integer, nullable=False
    )

    active: Mapped[bool] = mapped_column(
        Boolean, default=True, index=True
    )

    uploaded_by: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    course = relationship("Course", back_populates="documents")
