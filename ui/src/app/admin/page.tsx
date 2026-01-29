"use client";

import { useEffect, useMemo, useState } from "react";
import {
  createCourse,
  createDepartment,
  listCourses,
  listCourseDocuments,
  uploadCourseDocument,
  logout,
} from "@/src/lib/api";
import type { Course, DocumentRecord } from "@/src/lib/types";
import { useAuthGuard } from "@/src/hooks/useAuthGuard";

type CourseOption = {
  id?: string;
  code: string;
  name: string;
  department: string;
};

export default function AdminPage() {
  useAuthGuard();

  const [courses, setCourses] = useState<CourseOption[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string>("");
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [loadingDocs, setLoadingDocs] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  const [deptForm, setDeptForm] = useState({
    code: "",
    name: "",
    faculty: "",
  });

  const [courseForm, setCourseForm] = useState({
    code: "",
    name: "",
    department_code: "",
  });

  const [docForm, setDocForm] = useState({
    title: "",
    documentType: "lecture",
    file: null as File | null,
  });

  const coursesByDepartment = useMemo(() => {
    const map: Record<string, Course[]> = {};
    courses.forEach((c) => {
      map[c.department] = map[c.department] || [];
      map[c.department].push(c as Course);
    });
    return map;
  }, [courses]);

  async function refreshCourses() {
    setLoadingCourses(true);
    setError(null);
    try {
      const data = await listCourses();
      setCourses(data);
      if (!selectedCourse && data.length > 0) {
        setSelectedCourse(data[0].code);
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load courses");
    } finally {
      setLoadingCourses(false);
    }
  }

  async function refreshDocuments(courseId: string) {
    setLoadingDocs(true);
    setError(null);
    try {
      const data = await listCourseDocuments(courseId);
      setDocuments(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load documents");
    } finally {
      setLoadingDocs(false);
    }
  }

  useEffect(() => {
    refreshCourses();
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      refreshDocuments(selectedCourse);
    }
  }, [selectedCourse]);

  return (
    <main className="max-w-6xl mx-auto p-6 space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold">Admin Console</h1>
          <p className="text-sm text-gray-600">
            Govern departments, courses, and documents.
          </p>
        </div>
        <button
          className="text-sm underline"
          onClick={async () => {
            try {
              await logout();
              window.location.href = "/login";
            } catch (err) {
              setError(
                err instanceof Error ? err.message : "Unable to log out."
              );
            }
          }}
        >
          Logout
        </button>
      </div>

      {error && <p className="text-red-600">{error}</p>}
      {success && <p className="text-green-700">{success}</p>}

      <section className="grid md:grid-cols-2 gap-6">
        <div className="border rounded p-4 space-y-3">
          <h2 className="font-semibold">Create Department</h2>
          <div className="space-y-2">
            <input
              className="w-full border rounded p-2"
              placeholder="Code (e.g., CS)"
              value={deptForm.code}
              onChange={(e) =>
                setDeptForm({ ...deptForm, code: e.target.value })
              }
            />
            <input
              className="w-full border rounded p-2"
              placeholder="Name"
              value={deptForm.name}
              onChange={(e) =>
                setDeptForm({ ...deptForm, name: e.target.value })
              }
            />
            <input
              className="w-full border rounded p-2"
              placeholder="Faculty"
              value={deptForm.faculty}
              onChange={(e) =>
                setDeptForm({ ...deptForm, faculty: e.target.value })
              }
            />
          </div>
          <button
            className="bg-black text-white px-4 py-2 rounded"
            onClick={async () => {
              setError(null);
              setSuccess(null);
              try {
                await createDepartment(deptForm);
                setDeptForm({ code: "", name: "", faculty: "" });
                setSuccess("Department created.");
              } catch (err) {
                setError(
                  err instanceof Error
                    ? err.message
                    : "Failed to create department"
                );
              }
            }}
          >
            Create Department
          </button>
        </div>

        <div className="border rounded p-4 space-y-3">
          <h2 className="font-semibold">Create Course</h2>
          <div className="space-y-2">
            <input
              className="w-full border rounded p-2"
              placeholder="Course code (e.g., CS5589)"
              value={courseForm.code}
              onChange={(e) =>
                setCourseForm({ ...courseForm, code: e.target.value })
              }
            />
            <input
              className="w-full border rounded p-2"
              placeholder="Course name"
              value={courseForm.name}
              onChange={(e) =>
                setCourseForm({ ...courseForm, name: e.target.value })
              }
            />
            <input
              className="w-full border rounded p-2"
              placeholder="Department code"
              value={courseForm.department_code}
              onChange={(e) =>
                setCourseForm({
                  ...courseForm,
                  department_code: e.target.value,
                })
              }
            />
          </div>
          <button
            className="bg-black text-white px-4 py-2 rounded"
            onClick={async () => {
              setError(null);
              setSuccess(null);
              try {
                await createCourse(courseForm);
                setCourseForm({ code: "", name: "", department_code: "" });
                setSuccess("Course created.");
                await refreshCourses();
              } catch (err) {
                setError(
                  err instanceof Error
                    ? err.message
                    : "Failed to create course"
                );
              }
            }}
          >
            Create Course
          </button>
        </div>
      </section>

      <section className="border rounded p-4 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-semibold">Courses</h2>
          <button
            className="text-sm underline"
            onClick={() => refreshCourses()}
            disabled={loadingCourses}
          >
            {loadingCourses ? "Refreshing…" : "Refresh"}
          </button>
        </div>
        {Object.keys(coursesByDepartment).length === 0 && (
          <p className="text-sm text-gray-500">No courses found.</p>
        )}
        <div className="space-y-4">
          {Object.entries(coursesByDepartment).map(([dept, list]) => (
            <div key={dept} className="space-y-2">
              <h3 className="text-sm font-semibold">{dept}</h3>
              <div className="grid md:grid-cols-2 gap-3">
                {list.map((course) => (
                  <button
                    key={course.code}
                    className={`border rounded p-3 text-left ${
                      selectedCourse === course.code
                        ? "border-black"
                        : "border-gray-200"
                    }`}
                    onClick={() => setSelectedCourse(course.code)}
                  >
                    <div className="font-medium">{course.code}</div>
                    <div className="text-sm text-gray-600">{course.name}</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      </section>

      <section className="border rounded p-4 space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="font-semibold">Course Documents</h2>
          <div className="text-sm text-gray-600">
            Selected course: {selectedCourse || "None"}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div className="space-y-3">
            <h3 className="text-sm font-semibold">Upload document</h3>
            <input
              className="w-full border rounded p-2"
              placeholder="Title"
              value={docForm.title}
              onChange={(e) =>
                setDocForm({ ...docForm, title: e.target.value })
              }
            />
            <select
              className="w-full border rounded p-2"
              value={docForm.documentType}
              onChange={(e) =>
                setDocForm({ ...docForm, documentType: e.target.value })
              }
            >
              <option value="lecture">Lecture</option>
              <option value="notes">Notes</option>
              <option value="slides">Slides</option>
            </select>
            <input
              type="file"
              accept="application/pdf"
              onChange={(e) =>
                setDocForm({
                  ...docForm,
                  file: e.target.files?.[0] || null,
                })
              }
            />
            <button
              className="bg-black text-white px-4 py-2 rounded"
              onClick={async () => {
                setError(null);
                setSuccess(null);
                if (!selectedCourse) {
                  setError("Select a course first.");
                  return;
                }
                if (!docForm.file) {
                  setError("Choose a PDF to upload.");
                  return;
                }
                try {
                  await uploadCourseDocument({
                    courseId: selectedCourse,
                    title: docForm.title,
                    documentType: docForm.documentType,
                    file: docForm.file,
                  });
                  setDocForm({
                    title: "",
                    documentType: "lecture",
                    file: null,
                  });
                  setSuccess("Document uploaded and ingested.");
                  await refreshDocuments(selectedCourse);
                } catch (err) {
                  setError(
                    err instanceof Error
                      ? err.message
                      : "Failed to upload document"
                  );
                }
              }}
            >
              Upload
            </button>
          </div>

          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-semibold">Document list</h3>
              <button
                className="text-sm underline"
                onClick={() =>
                  selectedCourse && refreshDocuments(selectedCourse)
                }
                disabled={loadingDocs}
              >
                {loadingDocs ? "Refreshing…" : "Refresh"}
              </button>
            </div>
            {documents.length === 0 ? (
              <p className="text-sm text-gray-500">
                No documents uploaded for this course.
              </p>
            ) : (
              <div className="space-y-2 text-sm">
                {documents.map((doc) => (
                  <div
                    key={doc.id}
                    className="border rounded p-2 space-y-1"
                  >
                    <div className="font-medium">{doc.title}</div>
                    <div className="text-gray-600">
                      Type: {doc.document_type} • v{doc.version} •{" "}
                      {doc.active ? "Active" : "Inactive"}
                    </div>
                    <div className="text-gray-500">
                      Uploaded by: {doc.uploaded_by}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </section>

      <section className="border rounded p-4 space-y-2">
        <h2 className="font-semibold">Observability</h2>
        <p className="text-sm text-gray-600">
          Ingestion logs, error events, and chunk counts are not exposed yet.
          Once endpoints are available, this panel will show ingestion status
          and recent admin actions.
        </p>
      </section>
    </main>
  );
}
