
"use client";

import { useState } from "react";

export function AskForm({
  onSubmit,
}: {
  onSubmit: (q: string, c?: string) => void;
}) {
  const [question, setQuestion] = useState("");
  const [courseCode, setCourseCode] = useState("");

  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(question, courseCode);
      }}
    >
      <textarea
        className="w-full border rounded p-3"
        rows={4}
        placeholder="Ask a course-related question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        required
      />

      <input
        className="w-full border rounded p-2"
        placeholder="Course code (optional, e.g. CS5589)"
        value={courseCode}
        onChange={(e) => setCourseCode(e.target.value)}
      />

      <button
        className="bg-black text-white px-4 py-2 rounded"
        type="submit"
      >
        Ask Canon
      </button>
    </form>
  );
}