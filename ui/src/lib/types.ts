
export type Citation = {
  document: string;
  chunk: number | null;
  ref?: string | null;
};

export type FollowUpType =
  | "clarify_or_general"
  | "ask_general"
  | "conceptual_help";

export type AskResponse = {
  answer: string;
  source: string;
  confidence: "high" | "medium" | "low" | "none";
  citations: Citation[];
  follow_up?: FollowUpType | null;
};

export type LoginResponse = {
  access_token: string;
  refresh_token?: string;
};

export type Department = {
  id?: string;
  code: string;
  name: string;
  faculty: string;
};

export type Course = {
  id?: string;
  code: string;
  name: string;
  department: string;
  department_id?: string;
};

export type DocumentRecord = {
  id: string;
  title: string;
  document_type: string;
  version: number;
  active: boolean;
  uploaded_by: string;
};

export type AdminLogEntry = {
  type: string;
  timestamp: string;
  request_id?: string;
  department_code?: string;
  department_id?: string;
  course_code?: string;
  course_id?: string;
  document_id?: string;
  title?: string;
  document_type?: string;
  version?: number;
};

export type DocumentStatus = {
  document_id: string;
  course_id: string;
  title: string;
  document_type: string;
  version: number;
  active: boolean;
  chunk_count: number;
  index_size: number;
};
