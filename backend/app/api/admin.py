from fastapi import APIRouter, HTTPException, UploadFile
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
from app.core.admin_auth import require_admin
from app.schemas.admin import DepartmentCreate, CourseCreate
from app.service.admin import (create_department_service,
    create_course_service,
)

from app.rag.ingest import chunk_text, load_pdf, make_chunks

router = APIRouter(prefix="/admin", tags=["admin"])
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/departments", dependencies=[Depends(require_admin)])
def create_department(
    payload: DepartmentCreate,
    db: Session = Depends(get_db),
):
    department = create_department_service(db, payload)
    return {
        "id": department.id,
        "code": department.code,
        "name": department.name,
        "faculty": department.faculty,
    }


@router.post("/courses", dependencies=[Depends(require_admin)])
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
):
    course = create_course_service(db, payload)
    return {
        "id": course.id,
        "code": course.code,
        "name": course.name,
        "department_id": course.department_id,
    }





@router.post(
    "/courses/{course_code}/documents",
    dependencies=[Depends(require_admin)],
)
async def upload_course_document(
    course_code: str,
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form("lecture"),
):
    course = get_course_by_code(db, course_code)

    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Save file
    file_path = os.path.join(
        UPLOAD_DIR, f"{course_code}_{file.filename}"
    )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ingest
    text = load_pdf(file_path)
    chunks = make_chunks(
        text,
        department=course.department.code,  # ✅ FK-resolved
        course_code=course.code,
        document=title,
        document_type=document_type,
    )

    vector_store.add(chunks)

    return {
        "message": "Document uploaded",
        "course_code": course.code,
        "course_id": course.id,
        "title": title,
        "document_type": document_type,
    }

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