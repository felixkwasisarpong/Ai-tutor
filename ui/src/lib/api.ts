import type { AskResponse, LoginResponse } from "@/src/lib/types";
import {
  getRefreshToken,
  getToken,
  setRefreshToken,
  setToken,
  clearToken,
} from "@/src/lib/auth";

const API_BASE_URL = "http://localhost:8000";

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
    throw new Error("Failed to log out");
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
