"use client";

import { useState } from "react";
import { AskForm } from "@/src/components/AskForm";
import { useAuthGuard } from "@/src/hooks/useAuthGuard";
import { askQuestion, logout } from "@/src/lib/api";
import type { AskResponse } from "@/src/lib/types";

export default function StudentPage() {
  useAuthGuard("student");

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

  function detectLanguage(code: string) {
    const snippet = code.trim();
    if (!snippet) return "text";
    if (snippet.includes("import React") || snippet.includes("useState(")) {
      return "tsx";
    }
    if (snippet.includes("console.log(") || snippet.includes("export default")) {
      return "javascript";
    }
    if (snippet.includes("def ") || snippet.includes("import ") && snippet.includes(":")) {
      return "python";
    }
    if (snippet.includes("#include") || snippet.includes("std::")) {
      return "cpp";
    }
    if (snippet.includes("public class") || snippet.includes("System.out")) {
      return "java";
    }
    if (snippet.includes("SELECT ") || snippet.includes("FROM ")) {
      return "sql";
    }
    if (snippet.includes("func ") || snippet.includes("package ")) {
      return "go";
    }
    if (snippet.includes("<!DOCTYPE html>") || snippet.includes("<html")) {
      return "html";
    }
    if (snippet.includes("{") && snippet.includes("}")) {
      return "code";
    }
    return "text";
  }

  function renderAnswer(answer: string) {
    const parts: Array<{ type: "text" | "code"; content: string; lang?: string }> = [];
    const regex = /```([\w+-]*)\n([\s\S]*?)```/g;
    let lastIndex = 0;
    let match: RegExpExecArray | null;

    while ((match = regex.exec(answer)) !== null) {
      if (match.index > lastIndex) {
        parts.push({ type: "text", content: answer.slice(lastIndex, match.index) });
      }
      const lang = match[1] || detectLanguage(match[2]);
      parts.push({ type: "code", content: match[2], lang });
      lastIndex = regex.lastIndex;
    }

    if (lastIndex < answer.length) {
      parts.push({ type: "text", content: answer.slice(lastIndex) });
    }

    return (
      <div className="space-y-4 text-slate-900">
        {parts.map((part, idx) => {
          if (part.type === "code") {
            return (
              <div key={`code-${idx}`} className="rounded-xl border border-slate-200 bg-slate-900 text-slate-100 overflow-hidden">
                <div className="flex items-center justify-between px-4 py-2 text-xs text-slate-300 bg-slate-800">
                  <span>{part.lang || "code"}</span>
                  <span>```</span>
                </div>
                <pre className="p-4 overflow-x-auto text-sm">
                  <code>{part.content}</code>
                </pre>
              </div>
            );
          }
          return (
            <p key={`text-${idx}`} className="text-sm text-slate-800 whitespace-pre-wrap">
              {part.content.trim()}
            </p>
          );
        })}
      </div>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-slate-50 via-white to-slate-50">
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        <header className="rounded-2xl border border-slate-200 bg-white/70 backdrop-blur p-6 shadow-sm">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-slate-200 px-3 py-1 text-xs uppercase tracking-wide text-slate-500">
                Student Workspace
              </div>
              <h1 className="mt-3 text-3xl font-semibold text-slate-900">
                Ask Canon
              </h1>
              <p className="mt-2 text-sm text-slate-600">
                Ask course-grounded questions and receive citations.
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
                    err instanceof Error
                      ? err.message
                      : "Unable to log out."
                  );
                }
              }}
            >
              Logout
            </button>
          </div>
        </header>

        {(error || loading) && (
          <div className="grid gap-3 md:grid-cols-2">
            {loading && (
              <div className="rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-600">
                <div className="flex items-center gap-3">
                  <div className="h-2 w-2 rounded-full bg-slate-500 animate-pulse" />
                  <div className="h-2 w-2 rounded-full bg-slate-400 animate-pulse [animation-delay:150ms]" />
                  <div className="h-2 w-2 rounded-full bg-slate-300 animate-pulse [animation-delay:300ms]" />
                  <span className="text-sm text-slate-600">
                    Thinking…
                  </span>
                </div>
              </div>
            )}
            {error && (
              <div className="rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700">
                {error}
              </div>
            )}
          </div>
        )}

        <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-800">
            New Academic Request
          </h2>
          <p className="mt-1 text-sm text-slate-500">
            Provide a question, optional course code, and a supporting file.
          </p>
          <div className="mt-4">
            <AskForm onSubmit={handleAsk} />
          </div>
        </section>

        {result && (
          <section className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm space-y-4">
            <div className="flex flex-wrap items-center gap-2 text-xs">
              <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
                Confidence:{" "}
                <span className="font-semibold">{result.confidence}</span>
              </span>
              <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
                Citations:{" "}
                <span className="font-semibold">
                  {result.citations.length}
                </span>
              </span>
              {result.confidence === "none" && (
                <span className="rounded-full bg-red-100 px-3 py-1 text-red-700">
                  No answer available
                </span>
              )}
              {result.source && (
                <span className="rounded-full bg-slate-100 px-3 py-1 text-slate-600">
                  Source: {result.source}
                </span>
              )}
            </div>

            <div className="rounded-xl border border-slate-100 bg-slate-50 p-4">
              {renderAnswer(result.answer)}
            </div>

            {result.citations.length > 0 && (
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-xs uppercase tracking-wide text-slate-500">
                    Citations
                  </span>
                  <span className="h-px flex-1 bg-slate-200" />
                </div>
                <ul className="grid gap-2 md:grid-cols-2">
                  {result.citations.map((c, i) => (
                    <li
                      key={i}
                      className="rounded-lg border border-slate-200 bg-white p-3 text-slate-700"
                    >
                      <div className="text-sm font-medium">
                        {c.document}
                      </div>
                      <div className="text-xs text-slate-500">
                        Chunk {c.chunk ?? "—"}
                      </div>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {result.follow_up && !followUpDismissed && (
              <div className="rounded-xl border border-amber-200 bg-amber-50 p-4 space-y-3">
                <p className="text-sm text-amber-800">
                  Follow-up suggested: {result.follow_up}
                </p>
                <textarea
                  className="w-full rounded-lg border border-amber-200 p-2 text-sm"
                  rows={2}
                  placeholder="Add a clarification (optional)..."
                  value={followUpText}
                  onChange={(e) => setFollowUpText(e.target.value)}
                />
                <div className="flex flex-wrap gap-2">
                  {result.follow_up === "clarify_or_general" && (
                    <>
                      <button
                        className="rounded-full border border-amber-300 px-4 py-2 text-sm text-amber-900 hover:bg-amber-100"
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
                        className="rounded-full border border-amber-300 px-4 py-2 text-sm text-amber-900 hover:bg-amber-100"
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
                      className="rounded-full border border-amber-300 px-4 py-2 text-sm text-amber-900 hover:bg-amber-100"
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
                      className="rounded-full border border-amber-300 px-4 py-2 text-sm text-amber-900 hover:bg-amber-100"
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
                    className="text-sm text-amber-800 underline"
                    onClick={() => setFollowUpDismissed(true)}
                  >
                    Dismiss
                  </button>
                </div>
              </div>
            )}
          </section>
        )}
      </div>
    </main>
  );
}
