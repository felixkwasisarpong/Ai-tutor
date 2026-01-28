"use client";
import { useOCR } from "@/src/hooks/useOCR";
import { useState } from "react";
import { useSpeechToText } from "@/src/hooks/useSpeechToText";
export function AskForm({
  onSubmit,
}: {
  onSubmit: (
    q: string,
    c?: string,
    f?: File | null,
    extraText?: string
  ) => void;
}) {
  const [question, setQuestion] = useState("");
  const [courseCode, setCourseCode] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const speech = useSpeechToText();
  const ocr = useOCR();
  return (
        <form
        onSubmit={(e) => {
            e.preventDefault();
            onSubmit(
            speech.transcript || question,
            courseCode,
            file,
            ocr.text
            );
        }}
        >
    <textarea
    className="w-full border rounded p-3"
    rows={4}
    placeholder="Ask a course-related question..."
    value={speech.transcript || question}
    onChange={(e) => setQuestion(e.target.value)}
    required
    />
<div className="flex gap-2">
  <button
    type="button"
    onClick={speech.start}
    className="border px-3 py-1 rounded"
  >
    🎙️ Speak
  </button>

  {speech.listening && (
    <span className="text-sm text-gray-500">Listening…</span>
  )}

  {speech.transcript && (
    <button
      type="button"
      onClick={speech.reset}
      className="text-sm underline"
    >
      Clear voice input
    </button>
  )}
</div>
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

        <input
        type="file"
        accept="image/*"
        onChange={(e) => {
            const file = e.target.files?.[0];
            if (file) {
            ocr.extract(file);
            }
        }}
        />
        {ocr.loading && (
    <p className="text-sm text-gray-500">Extracting text from image…</p>
    )}

    {ocr.text && (
    <div className="text-sm border p-2 rounded bg-gray-50">
        <p className="font-medium">Extracted text (editable):</p>
        <textarea
        className="w-full border mt-1 p-2"
        rows={3}
        value={ocr.text}
        onChange={(e) => ocr.reset()}
        readOnly
        />
    </div>
    )}
      <button
        className="bg-black text-white px-4 py-2 rounded"
        type="submit"
      >
        Ask Canon
      </button>
    </form>
  );
}