"use client";

import { useRef, useState } from "react";

type WebkitSpeechRecognition = {
  lang: string;
  continuous: boolean;
  interimResults: boolean;
  onstart: (() => void) | null;
  onend: (() => void) | null;
  onresult: ((event: WebkitSpeechRecognitionEvent) => void) | null;
  start: () => void;
  stop: () => void;
};

type WebkitSpeechRecognitionEvent = {
  results: ArrayLike<ArrayLike<{ transcript: string }>>;
};

declare global {
  interface Window {
    webkitSpeechRecognition?: {
      new (): WebkitSpeechRecognition;
    };
  }
}

export function useSpeechToText() {
  const [listening, setListening] = useState(false);
  const [transcript, setTranscript] = useState("");
  const recognitionRef = useRef<WebkitSpeechRecognition | null>(null);

  function start() {
    if (!window.webkitSpeechRecognition) {
      alert("Speech recognition not supported in this browser");
      return;
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      setTranscript(text);
    };

    recognitionRef.current = recognition;
    recognition.start();
  }

  function stop() {
    recognitionRef.current?.stop();
  }

  function reset() {
    setTranscript("");
  }

  return {
    transcript,
    listening,
    start,
    stop,
    reset,
  };
}
