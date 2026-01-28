"use client";

import { useState } from "react";
import { askQuestion } from "@/src/lib/api";
import { AskForm } from "@/src/components/AskForm";
import { AnswerCard } from "@/src/components/AnswerCard";
import { AskResponse } from "@/src/lib/types";

export default function StudentPage() {
  const [result, setResult] = useState<AskResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleAsk(question: string, courseCode?: string) {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const res = await askQuestion(question, courseCode);
      setResult(res);
    } catch {
      setError("Unable to get an answer.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="max-w-3xl mx-auto py-10">
      <h1 className="text-3xl font-bold mb-6">Canon — Student Portal</h1>

      <AskForm onSubmit={handleAsk} />

      {loading && <p className="mt-4">Thinking…</p>}
      {error && <p className="mt-4 text-red-600">{error}</p>}
      {result && <AnswerCard result={result} />}
    </main>
  );
}
