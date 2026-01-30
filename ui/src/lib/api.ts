import type {
  AskResponse,
  LoginResponse,
  Department,
  Course,
  DocumentRecord,
  AdminLogEntry,
  DocumentStatus,
} from "@/src/lib/types";
import {
  getRefreshToken,
  getToken,
  setRefreshToken,
  setToken,
  clearToken,
} from "@/src/lib/auth";


export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export async function login(
  email: string,
  password: string
): Promise<LoginResponse> {
  const res = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email, password }),
  });

  if (!res.ok) {
    throw new Error("Invalid credentials");
  }

  const data = (await res.json()) as LoginResponse;
  if (!data?.access_token) {
    throw new Error("Missing access token");
  }

  setToken(data.access_token);
  if (data.refresh_token) {
    setRefreshToken(data.refresh_token);
  }

  return data;
}

export async function refreshAccessToken(): Promise<{
  access_token: string;
}> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    throw new Error("Missing refresh token");
  }

  const res = await fetch(`${API_BASE_URL}/auth/refresh`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!res.ok) {
    throw new Error("Failed to refresh token");
  }

  const data = (await res.json()) as { access_token: string };
  if (!data?.access_token) {
    throw new Error("Missing access token");
  }

  setToken(data.access_token);
  return data;
}

export async function logout(): Promise<void> {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    clearToken();
    return;
  }

  const res = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ refresh_token: refreshToken }),
  });

  if (!res.ok) {
    let message = "Failed to log out";
    try {
      const data = await res.json();
      if (data?.detail) {
        message = data.detail;
      }
    } catch {
      // ignore parse errors
    }
    throw new Error(message);
  }

  clearToken();
}

export async function askQuestion(params: {
  question: string;
  courseCode?: string;
  file?: File | null;
  supplementalText?: string;
}): Promise<AskResponse> {
  const token = getToken();
  if (!token) {
    throw new Error("Missing access token");
  }

  const formData = new FormData();
  formData.append("question", params.question);
  if (params.courseCode) {
    formData.append("course_code", params.courseCode);
  }
  if (params.file) {
    formData.append("file", params.file);
  }
  if (params.supplementalText) {
    formData.append("extra_context", params.supplementalText);
  }

  let res = await fetch(`${API_BASE_URL}/ask`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: formData,
  });

  if (res.status === 401) {
    try {
      await refreshAccessToken();
      const refreshedToken = getToken();
      if (!refreshedToken) {
        throw new Error("Missing access token");
      }
      res = await fetch(`${API_BASE_URL}/ask`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${refreshedToken}`,
        },
        body: formData,
      });
    } catch {
      clearToken();
      throw new Error("Session expired. Please log in again.");
    }
  }

  if (!res.ok) {
    throw new Error("Failed to get answer");
  }

  return res.json();
}

async function adminFetch(
  path: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = getToken();
  if (!token) {
    throw new Error("Missing access token");
  }

  const res = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401) {
    await refreshAccessToken();
    const refreshedToken = getToken();
    if (!refreshedToken) {
      throw new Error("Missing access token");
    }
    return fetch(`${API_BASE_URL}${path}`, {
      ...options,
      headers: {
        ...(options.headers || {}),
        Authorization: `Bearer ${refreshedToken}`,
      },
    });
  }

  return res;
}

export async function createDepartment(
  payload: Department
): Promise<Department> {
  const res = await adminFetch("/admin/departments", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to create department");
  }

  return res.json();
}

export async function createCourse(payload: {
  code: string;
  name: string;
  department_code: string;
}): Promise<Course> {
  const res = await adminFetch("/admin/courses", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    throw new Error("Failed to create course");
  }

  return res.json();
}

export async function listCourses(): Promise<Course[]> {
  const res = await adminFetch("/admin/courses", {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to load courses");
  }

  return res.json();
}

export async function uploadCourseDocument(params: {
  courseId: string;
  title: string;
  documentType?: string;
  file: File;
}): Promise<{
  document_id: string;
  version: number;
  status: string;
}> {
  const formData = new FormData();
  formData.append("title", params.title);
  formData.append("document_type", params.documentType || "lecture");
  formData.append("file", params.file);

  const res = await adminFetch(
    `/admin/courses/${params.courseId}/documents`,
    {
      method: "POST",
      body: formData,
    }
  );

  if (!res.ok) {
    throw new Error("Failed to upload document");
  }

  return res.json();
}

export async function listCourseDocuments(
  courseId: string
): Promise<DocumentRecord[]> {
  const res = await adminFetch(`/admin/courses/${courseId}/documents`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to load documents");
  }

  return res.json();
}

export async function listAdminLogs(
  limit = 50
): Promise<AdminLogEntry[]> {
  const res = await adminFetch(`/admin/logs?limit=${limit}`, {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error("Failed to load admin logs");
  }

  return res.json();
}

export async function getDocumentStatus(
  documentId: string
): Promise<DocumentStatus> {
  const res = await adminFetch(
    `/admin/documents/${documentId}/status`,
    {
      method: "GET",
    }
  );

  if (!res.ok) {
    throw new Error("Failed to load document status");
  }

  return res.json();
}
