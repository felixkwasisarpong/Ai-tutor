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
          <p>{result.answer}</p>

          {result.confidence && (
            <p className="text-sm text-gray-500">
              Confidence: <strong>{result.confidence}</strong>
            </p>
          )}

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
        </div>
      )}
    </main>
  );
}
