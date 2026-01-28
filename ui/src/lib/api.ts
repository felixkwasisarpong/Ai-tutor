export async function askQuestion(
  question: string,
  courseCode?: string
) {
  const res = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      question,
      course_code: courseCode || null,
    }),
  });

  if (!res.ok) {
    throw new Error("Failed to get answer");
  }

  return res.json();
}