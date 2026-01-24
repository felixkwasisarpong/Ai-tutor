from fastapi import APIRouter, HTTPException, UploadFile,Request
from pydantic import BaseModel
import os
from fastapi import File, Form, Depends
from uuid import UUID
import shutil
from app.rag.store import vector_store
from app.core.course_registry import get_course_by_code, get_all_courses
from app.service.courses import get_course_by_code, list_courses
from app.db.deps import get_db
from sqlalchemy.orm import Session
from app.core.dependencies import require_admin
from app.schemas.admin import DepartmentCreate, CourseCreate
from app.service.document_service import next_document_version
from app.db.models.document import Document
import uuid
from app.service.admin import (create_department_service,
    create_course_service,
)

from app.db.models.course import Course
from app.core.logging import logger
from app.rag.ingest import chunk_text, load_pdf, make_chunks

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/departments")
def create_department(
    payload: DepartmentCreate,
    request: Request,     
    db: Session = Depends(get_db),
):
    
    logger.info(
    "Admin action",
    extra={
        "action": "create_department",
        "course_code": payload.code,
        "request_id": request.state.request_id,
    },
)
    department = create_department_service(db, payload)
    return {
        "id": department.id,
        "code": department.code,
        "name": department.name,
        "faculty": department.faculty,
    }


@router.post("/courses")
def create_course(
    payload: CourseCreate,
    request: Request,
    db: Session = Depends(get_db),
):
    
    logger.info(
    "Admin action",
    extra={
        "action": "create_course",
        "course_code": payload.code,
        "request_id": request.state.request_id,
    },
)
    course = create_course_service(db, payload)
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "department_id": course.department_id,
    }





@router.post(
    "/courses/{course_id}/documents",
)
async def upload_course_document(
    course_id: str,
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form("lecture"),
    db: Session = Depends(get_db),
    admin: str = Depends(require_admin),
):
    course = get_course_by_id_or_code(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    version = next_document_version(
        db,
        course_id=course.id,
        title=title,
        document_type=document_type,
    )

    # Deactivate previous versions
    (
        db.query(Document)
        .filter(
            Document.course_id == course.id,
            Document.title == title,
            Document.active == True,
        )
        .update({"active": False})
    )

    document = Document(
        course_id=course.id,
        title=title,
        document_type=document_type,
        version=version,
        uploaded_by=admin,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    # Save file path includes version
    file_path = f"data/{course.code}/{title}_v{version}.pdf"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Ingest with version metadata
    chunks = make_chunks(
        load_pdf(file_path),
        course_code=course.code,
        document=title,
        document_type=document_type,
        version=version,
        document_id=str(document.id),
    )

    vector_store.add(chunks)

    return {
        "document_id": document.id,
        "version": version,
        "status": "uploaded",
    }

def get_course_by_id_or_code(db: Session, course_key: str) -> Course | None:
    course = None
    try:
        course_uuid = UUID(course_key)
    except ValueError:
        course_uuid = None

    if course_uuid is not None:
        course = db.get(Course, course_uuid)

    if not course:
        course = get_course_by_code(db, course_key)

    return course


@router.get("/courses/{course_id}/documents", dependencies=[Depends(require_admin)])
def list_course_documents(
    course_id: str,
    db: Session = Depends(get_db),
):
    course = get_course_by_id_or_code(db, course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    documents = (
        db.query(Document)
        .filter(Document.course_id == course.id)
        .order_by(Document.title, Document.version.desc())
        .all()
    )

    return [
        {
            "id": d.id,
            "title": d.title,
            "document_type": d.document_type,
            "version": d.version,
            "active": d.active,
            "uploaded_by": d.uploaded_by,
        }
        for d in documents
    ]

@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = list_courses(db)
    return [
        {
            "code": c.code,
            "name": c.name,
            "department": c.department.code,
        }
        for c in courses
    ]
