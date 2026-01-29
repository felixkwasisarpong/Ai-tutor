"use client";

import { useState } from "react";
import { AskForm } from "@/src/components/AskForm";
import { useAuthGuard } from "@/src/hooks/useAuthGuard";
import { askQuestion } from "@/src/lib/api";
import type { AskResponse } from "@/src/lib/types";

export default function StudentPage() {
  useAuthGuard();

  const [result, setResult] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [lastQuestion, setLastQuestion] = useState<string | null>(null);
  const [lastCourseCode, setLastCourseCode] = useState<string | undefined>();
  const [followUpText, setFollowUpText] = useState("");
  const [followUpDismissed, setFollowUpDismissed] = useState(false);

  async function handleAsk(
    question: string,
    courseCode?: string,
    file?: File | null,
    extraText?: string
  ) {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const data = await askQuestion({
        question,
        courseCode,
        file,
        supplementalText: extraText,
      });
      setResult(data);
      setLastQuestion(question);
      setLastCourseCode(courseCode);
      setFollowUpText("");
      setFollowUpDismissed(false);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Unable to get an answer."
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Ask Canon</h1>

      <AskForm onSubmit={handleAsk} />

      {loading && <p className="text-gray-500">Thinking…</p>}
      {error && <p className="text-red-600">{error}</p>}

      {result && (
        <div className="border rounded p-4 space-y-3">
          <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="px-2 py-0.5 rounded bg-gray-100">
              Confidence: <strong>{result.confidence}</strong>
            </span>
            <span className="px-2 py-0.5 rounded bg-gray-100">
              Citations: <strong>{result.citations.length}</strong>
            </span>
            {result.confidence === "none" && (
              <span className="px-2 py-0.5 rounded bg-red-100 text-red-700">
                No answer available
              </span>
            )}
          </div>

          <p>{result.answer}</p>

          {result.citations.length > 0 && (
            <div className="text-sm">
              <p className="font-medium">Citations</p>
              <ul className="list-disc pl-5">
                {result.citations.map((c, i) => (
                  <li key={i}>
                    {c.document} (chunk {c.chunk})
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.follow_up && !followUpDismissed && (
            <div className="border-t pt-3 space-y-2">
              <p className="text-sm text-orange-700">
                Follow-up suggested: {result.follow_up}
              </p>
              <textarea
                className="w-full border rounded p-2"
                rows={2}
                placeholder="Add a clarification (optional)..."
                value={followUpText}
                onChange={(e) => setFollowUpText(e.target.value)}
              />
              <div className="flex flex-wrap gap-2">
                {result.follow_up === "clarify_or_general" && (
                  <>
                    <button
                      className="border px-3 py-1 rounded"
                      onClick={() =>
                        handleAsk(
                          followUpText || lastQuestion || "",
                          lastCourseCode
                        )
                      }
                    >
                      Clarify with course material
                    </button>
                    <button
                      className="border px-3 py-1 rounded"
                      onClick={() =>
                        handleAsk(
                          followUpText || lastQuestion || "",
                          undefined
                        )
                      }
                    >
                      Ask as general question
                    </button>
                  </>
                )}
                {result.follow_up === "ask_general" && (
                  <button
                    className="border px-3 py-1 rounded"
                    onClick={() =>
                      handleAsk(
                        followUpText || lastQuestion || "",
                        undefined
                      )
                    }
                  >
                    Ask as general question
                  </button>
                )}
                {result.follow_up === "conceptual_help" && (
                  <button
                    className="border px-3 py-1 rounded"
                    onClick={() =>
                      handleAsk(
                        followUpText || lastQuestion || "",
                        undefined
                      )
                    }
                  >
                    Ask for conceptual help
                  </button>
                )}
                <button
                  className="text-sm underline"
                  onClick={() => setFollowUpDismissed(true)}
                >
                  Dismiss
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
