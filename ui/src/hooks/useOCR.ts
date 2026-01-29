"use client";

import { useState } from "react";
import Tesseract from "tesseract.js";

export function useOCR() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);

  async function extract(file: File) {
    setLoading(true);
    const result = await Tesseract.recognize(file, "eng");
    setText(result.data.text);
    setLoading(false);
  }

  function reset() {
    setText("");
  }

  return {
    text,
    setText,
    loading,
    extract,
    reset,
  };
}
