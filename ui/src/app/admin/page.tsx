"use client";

import { useEffect, useMemo, useState } from "react";
import {
  createCourse,
  createDepartment,
  listCourses,
  listCourseDocuments,
  uploadCourseDocument,
  logout,
  listAdminLogs,
  getDocumentStatus,
} from "@/src/lib/api";
import type {
  Course,
  DocumentRecord,
  AdminLogEntry,
  DocumentStatus,
} from "@/src/lib/types";
import { useAuthGuard } from "@/src/hooks/useAuthGuard";

type CourseOption = {
  id?: string;
  code: string;
  name: string;
  department: string;
};

export default function AdminPage() {
  useAuthGuard("admin");

  const [courses, setCourses] = useState<CourseOption[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<string>("");
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [documentStatus, setDocumentStatus] = useState<
    Record<string, DocumentStatus>
  >({});
  const [loadingCourses, setLoadingCourses] = useState(false);
  const [loadingDocs, setLoadingDocs] = useState(false);
  const [loadingLogs, setLoadingLogs] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [logs, setLogs] = useState<AdminLogEntry[]>([]);

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
      setDocumentStatus({});
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load documents");
    } finally {
      setLoadingDocs(false);
    }
  }

  async function refreshLogs() {
    setLoadingLogs(true);
    setError(null);
    try {
      const data = await listAdminLogs(50);
      setLogs(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load logs");
    } finally {
      setLoadingLogs(false);
    }
  }

  useEffect(() => {
    refreshCourses();
    refreshLogs();
  }, []);

  useEffect(() => {
    if (selectedCourse) {
      refreshDocuments(selectedCourse);
    }
  }, [selectedCourse]);

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <div className="max-w-6xl mx-auto p-6 space-y-8">
        <header className="rounded-2xl border border-slate-200 bg-white/70 backdrop-blur p-6 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 px-3 py-1 text-xs uppercase tracking-wide text-slate-500">
                Governance Console
              </div>
              <h1 className="mt-3 text-3xl font-semibold text-slate-900">
                Admin Control Center
              </h1>
              <p className="mt-2 text-sm text-slate-600">
                Curate departments, courses, and vetted source documents.
              </p>
            </div>
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
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
        </header>

        {(error || success) && (
          <div className="grid gap-3 md:grid-cols-2">
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {error}
              </div>
            )}
            {success && (
              <div className="rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-700">
                {success}
              </div>
            )}
          </div>
        )}

        <section className="grid gap-6 lg:grid-cols-2">
          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-800">
                Department Setup
              </h2>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                Org Structure
              </span>
            </div>
            <div className="mt-4 space-y-3">
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Code (e.g., CS)"
                value={deptForm.code}
                onChange={(e) =>
                  setDeptForm({ ...deptForm, code: e.target.value })
                }
              />
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Name"
                value={deptForm.name}
                onChange={(e) =>
                  setDeptForm({ ...deptForm, name: e.target.value })
                }
              />
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Faculty"
                value={deptForm.faculty}
                onChange={(e) =>
                  setDeptForm({ ...deptForm, faculty: e.target.value })
                }
              />
            </div>
            <button
              className="mt-4 w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
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

          <div className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-lg font-semibold text-slate-800">
                Course Setup
              </h2>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-xs text-slate-600">
                Curriculum
              </span>
            </div>
            <div className="mt-4 space-y-3">
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Course code (e.g., CS5589)"
                value={courseForm.code}
                onChange={(e) =>
                  setCourseForm({ ...courseForm, code: e.target.value })
                }
              />
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Course name"
                value={courseForm.name}
                onChange={(e) =>
                  setCourseForm({ ...courseForm, name: e.target.value })
                }
              />
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
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
              className="mt-4 w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
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

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold text-slate-800">Courses</h2>
              <p className="text-sm text-slate-500">
                Select a course to manage its source documents.
              </p>
            </div>
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
              onClick={() => refreshCourses()}
              disabled={loadingCourses}
            >
              {loadingCourses ? "Refreshing…" : "Refresh"}
            </button>
          </div>
          {Object.keys(coursesByDepartment).length === 0 && (
            <p className="mt-4 text-sm text-slate-500">No courses found.</p>
          )}
          <div className="mt-5 space-y-4">
            {Object.entries(coursesByDepartment).map(([dept, list]) => (
              <div key={dept} className="space-y-2">
                <div className="flex items-center gap-2 text-sm font-semibold text-slate-700">
                  <span className="rounded-full bg-slate-100 px-3 py-1">
                    {dept}
                  </span>
                  <span className="text-xs text-slate-500">
                    {list.length} courses
                  </span>
                </div>
                <div className="grid gap-3 md:grid-cols-2">
                  {list.map((course) => (
                    <button
                      key={course.code}
                      className={`rounded-xl border p-4 text-left transition ${
                        selectedCourse === course.code
                          ? "border-slate-900 bg-slate-50"
                          : "border-slate-200 hover:border-slate-400"
                      }`}
                      onClick={() => setSelectedCourse(course.code)}
                    >
                      <div className="flex items-center justify-between">
                        <div className="text-base font-semibold text-slate-800">
                          {course.code}
                        </div>
                        {selectedCourse === course.code && (
                          <span className="rounded-full bg-slate-900 px-2 py-1 text-xs text-white">
                            Active
                          </span>
                        )}
                      </div>
                      <div className="mt-1 text-sm text-slate-600">
                        {course.name}
                      </div>
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-lg font-semibold text-slate-800">
                Course Documents
              </h2>
              <p className="text-sm text-slate-500">
                Selected course:{" "}
                <span className="font-medium text-slate-700">
                  {selectedCourse || "None"}
                </span>
              </p>
            </div>
          </div>

          <div className="mt-5 grid gap-6 lg:grid-cols-[1.1fr_1.4fr]">
            <div className="space-y-4 rounded-xl border border-slate-200 bg-slate-50 p-4">
              <div className="flex items-center justify-between">
                <h3 className="text-sm font-semibold text-slate-700">
                  Upload document
                </h3>
                <span className="rounded-full bg-white px-3 py-1 text-xs text-slate-500">
                  PDF only
                </span>
              </div>
              <input
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
                placeholder="Title"
                value={docForm.title}
                onChange={(e) =>
                  setDocForm({ ...docForm, title: e.target.value })
                }
              />
              <select
                className="w-full rounded-lg border border-slate-200 p-3 text-sm focus:border-slate-400 focus:outline-none"
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
                className="w-full rounded-lg bg-slate-900 px-4 py-2 text-sm font-medium text-white hover:bg-slate-800"
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
                <h3 className="text-sm font-semibold text-slate-700">
                  Document list
                </h3>
                <button
                  className="rounded-full border border-slate-300 px-4 py-2 text-xs text-slate-700 hover:bg-slate-100"
                  onClick={() =>
                    selectedCourse && refreshDocuments(selectedCourse)
                  }
                  disabled={loadingDocs}
                >
                  {loadingDocs ? "Refreshing…" : "Refresh"}
                </button>
              </div>
              {documents.length === 0 ? (
                <div className="rounded-xl border border-dashed border-slate-200 p-6 text-center text-sm text-slate-500">
                  No documents uploaded for this course.
                </div>
              ) : (
                <div className="space-y-3 text-sm">
                  {documents.map((doc) => (
                    <div
                      key={doc.id}
                      className="rounded-xl border border-slate-200 bg-white p-4 shadow-sm"
                    >
                      <div className="flex items-start justify-between gap-3">
                        <div>
                          <div className="text-base font-semibold text-slate-800">
                            {doc.title}
                          </div>
                          <div className="mt-1 text-xs text-slate-500">
                            Uploaded by {doc.uploaded_by}
                          </div>
                        </div>
                        <div className="flex flex-col items-end gap-1 text-xs text-slate-600">
                          <span className="rounded-full bg-slate-100 px-2 py-1">
                            {doc.document_type}
                          </span>
                          <span className="rounded-full bg-slate-100 px-2 py-1">
                            v{doc.version}
                          </span>
                          <span
                            className={`rounded-full px-2 py-1 ${
                              doc.active
                                ? "bg-emerald-100 text-emerald-700"
                                : "bg-amber-100 text-amber-700"
                            }`}
                          >
                            {doc.active ? "Active" : "Inactive"}
                          </span>
                        </div>
                      </div>
                      {documentStatus[doc.id] && (
                        <div className="mt-2 text-xs text-slate-500">
                          Chunks indexed:{" "}
                          {documentStatus[doc.id].chunk_count}
                        </div>
                      )}
                      <button
                        className="mt-3 text-xs font-medium text-slate-700 underline"
                        onClick={async () => {
                          try {
                            const status = await getDocumentStatus(doc.id);
                            setDocumentStatus((prev) => ({
                              ...prev,
                              [doc.id]: status,
                            }));
                          } catch (err) {
                            setError(
                              err instanceof Error
                                ? err.message
                                : "Failed to load document status"
                            );
                          }
                        }}
                      >
                        View ingestion status
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </section>

        <section className="rounded-2xl border border-slate-200 bg-white p-5 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-semibold text-slate-800">
                Observability
              </h2>
              <p className="text-sm text-slate-500">
                Recent governance actions and ingestion events.
              </p>
            </div>
            <button
              className="rounded-full border border-slate-300 px-4 py-2 text-xs text-slate-700 hover:bg-slate-100"
              onClick={() => refreshLogs()}
              disabled={loadingLogs}
            >
              {loadingLogs ? "Refreshing…" : "Refresh"}
            </button>
          </div>
          {logs.length === 0 ? (
            <div className="mt-4 rounded-xl border border-dashed border-slate-200 p-6 text-center text-sm text-slate-500">
              No admin actions yet.
            </div>
          ) : (
            <div className="mt-4 grid gap-3 md:grid-cols-2">
              {logs.map((entry, idx) => (
                <div
                  key={`${entry.type}-${idx}`}
                  className="rounded-xl border border-slate-200 bg-slate-50 p-4"
                >
                  <div className="text-xs uppercase tracking-wide text-slate-500">
                    {entry.type}
                  </div>
                  <div className="mt-1 text-sm font-medium text-slate-800">
                    {entry.timestamp}
                  </div>
                  <div className="mt-2 text-xs text-slate-500">
                    Request: {entry.request_id || "no request id"}
                  </div>
                  {entry.course_code && (
                    <div className="mt-2 text-xs text-slate-600">
                      Course: {entry.course_code}
                    </div>
                  )}
                  {entry.department_code && (
                    <div className="text-xs text-slate-600">
                      Department: {entry.department_code}
                    </div>
                  )}
                  {entry.document_id && (
                    <div className="text-xs text-slate-600">
                      Document: {entry.document_id}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </section>
      </div>
    </main>
  );
}
