"use client";

import { useState } from "react";
import { AskForm } from "@/src/components/AskForm";
import { getToken } from "@/src/lib/auth";
import { useAuthGuard } from "@/src/hooks/useAuthGuard";

export default function StudentPage() {
  useAuthGuard();

  const [answer, setAnswer] = useState<string | null>(null);
  const [confidence, setConfidence] = useState<string | null>(null);
  const [citations, setCitations] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleAsk(question: string, courseCode?: string) {
    setLoading(true);
    setAnswer(null);

    const token = getToken();
    if (!token) return;

    const res = await fetch("http://localhost:8000/ask", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({
        question,
        course_code: courseCode || null,
      }),
    });

    const data = await res.json();

    setAnswer(data.answer);
    setConfidence(data.confidence);
    setCitations(data.citations || []);
    setLoading(false);
  }

  return (
    <main className="max-w-3xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-semibold">Ask Canon</h1>

      <AskForm onSubmit={handleAsk} />

      {loading && <p className="text-gray-500">Thinking…</p>}

      {answer && (
        <div className="border rounded p-4 space-y-3">
          <p>{answer}</p>

          {confidence && (
            <p className="text-sm text-gray-500">
              Confidence: <strong>{confidence}</strong>
            </p>
          )}

          {citations.length > 0 && (
            <div className="text-sm">
              <p className="font-medium">Citations</p>
              <ul className="list-disc pl-5">
                {citations.map((c, i) => (
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