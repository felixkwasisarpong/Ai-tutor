
export type Citation = {
  document: string;
  chunk: number | null;
  ref?: string | null;
};

export type AskResponse = {
  answer: string;
  source: string;
  confidence: "high" | "medium" | "low" | "none";
  citations: Citation[];
  follow_up?: string | null;
};