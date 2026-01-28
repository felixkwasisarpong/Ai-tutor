import { AskResponse } from "@/src/lib/types";

export function AnswerCard({ result }: { result: AskResponse }) {
  return (
    <div className="mt-6 border rounded p-4 bg-white">
      <p className="text-lg">{result.answer}</p>

      <div className="mt-4 text-sm text-gray-600">
        Confidence: <b>{result.confidence}</b>
      </div>

      {result.citations.length > 0 && (
        <div className="mt-4">
          <h4 className="font-semibold">Citations</h4>
          <ul className="list-disc list-inside text-sm">
            {result.citations.map((c, i) => (
              <li key={i}>
                {c.document} (chunk {c.chunk})
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.follow_up && (
        <div className="mt-4 italic text-orange-600">
          Suggested follow-up: clarify or narrow the question.
        </div>
      )}
    </div>
  );
}