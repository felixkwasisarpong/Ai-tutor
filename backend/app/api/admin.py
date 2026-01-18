from fastapi import APIRouter, HTTPException, UploadFile
from pydantic import BaseModel
import os
from fastapi import File, Form
from uuid import UUID
import shutil
from app.rag.store import vector_store
from app.core.course_registry import get_course_by_code, get_all_courses




from app.rag.ingest import chunk_text, load_pdf, make_chunks

router = APIRouter(prefix="/admin", tags=["admin"])
UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.get("/courses")
def list_courses():
    courses = get_all_courses()

    return [{
        "id": str(course.id),
        "code": course.code,
        "name": course.name,
        "department": course.department,
    }
    for course in courses

    ]

@router.post("/courses/{course_code}/documents")
async def upload_course_document(
    course_code: str,
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: str = Form("lecture"),
):
    try:
        course = get_course_by_code(course_code)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    course_id = course["id"]

    # Save file
    file_path = os.path.join(
        UPLOAD_DIR, f"{course_code}_{file.filename}"
    )
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Ingest
    text = load_pdf(file_path)
    chunks = make_chunks(
        chunk_text(text),
        department=course["department"],
        course_code=course_code,
        document=title,
    )

    vector_store.add(chunks)

    return {
        "status": "success",
        "course_code": course_code,
        "course_id": str(course_id),
        "document": title,
        "chunks_added": len(chunks),
    }