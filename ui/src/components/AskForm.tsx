"use client";

import { useState } from "react";

export function AskForm({
  onSubmit,
}: {
  onSubmit: (q: string, c?: string, f?: File | null) => void;
}) {
  const [question, setQuestion] = useState("");
  const [courseCode, setCourseCode] = useState("");
  const [file, setFile] = useState<File | null>(null);

  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(question, courseCode, file);
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

      <input
        type="file"
        accept="application/pdf"
        className="w-full"
        onChange={(e) => setFile(e.target.files?.[0] || null)}
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