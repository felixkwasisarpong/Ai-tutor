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
  const [ocrEditedText, setOcrEditedText] = useState("");
  return (
    <form
      className="space-y-4"
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(
          speech.transcript || question,
          courseCode,
          file,
          ocrEditedText || ocr.text
        );
      }}
    >
      <div className="rounded-2xl border border-slate-200 bg-white p-4 shadow-sm">
        <textarea
          className="w-full resize-none rounded-xl border border-slate-200 bg-slate-50 p-4 text-sm text-slate-800 focus:border-slate-400 focus:outline-none"
          rows={4}
          placeholder="Ask a course-related question..."
          value={speech.transcript || question}
          onChange={(e) => setQuestion(e.target.value)}
          required
        />

        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            type="button"
            onClick={speech.start}
            className="inline-flex items-center gap-2 rounded-full border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100"
          >
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-slate-900 text-white">
              🎙️
            </span>
            Voice input
          </button>

          {speech.listening && (
            <span className="text-sm text-emerald-600">
              Listening…
            </span>
          )}

          {speech.transcript && (
            <button
              type="button"
              onClick={speech.reset}
              className="text-sm text-slate-500 underline"
            >
              Clear voice input
            </button>
          )}

          <label className="ml-auto inline-flex items-center gap-2 rounded-full border border-slate-300 px-4 py-2 text-sm text-slate-700 hover:bg-slate-100 cursor-pointer">
            <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-slate-900 text-white">
              📎
            </span>
            {file ? "File attached" : "Attach file"}
            <input
              type="file"
              accept="application/pdf,image/*,audio/*"
              className="hidden"
              onChange={(e) => {
                const selected = e.target.files?.[0] || null;
                setFile(selected);
                if (selected?.type?.startsWith("image/")) {
                  ocr.extract(selected).then(() => {
                    setOcrEditedText(ocr.text);
                  });
                }
              }}
            />
          </label>
        </div>
      </div>

      <div className="grid gap-3 md:grid-cols-[1.2fr_1fr]">
        <input
          className="w-full rounded-xl border border-slate-200 bg-white p-3 text-sm text-slate-800 focus:border-slate-400 focus:outline-none"
          placeholder="Course code (optional, e.g. CS5589)"
          value={courseCode}
          onChange={(e) => setCourseCode(e.target.value)}
        />
        <button
          className="w-full rounded-xl bg-slate-900 px-4 py-3 text-sm font-medium text-white hover:bg-slate-800"
          type="submit"
        >
          Ask Canon
        </button>
      </div>

      {ocr.loading && (
        <div className="rounded-xl border border-slate-200 bg-slate-50 p-3 text-sm text-slate-600">
          Extracting text from image…
        </div>
      )}

      {ocr.text && (
        <div className="rounded-xl border border-slate-200 bg-white p-4 text-sm">
          <p className="font-medium text-slate-700">
            Extracted text (editable)
          </p>
          <textarea
            className="mt-2 w-full rounded-lg border border-slate-200 bg-slate-50 p-3 text-sm text-slate-700"
            rows={3}
            value={ocrEditedText || ocr.text}
            onChange={(e) => {
              setOcrEditedText(e.target.value);
              ocr.setText(e.target.value);
            }}
          />
        </div>
      )}
    </form>
  );
}
