
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
