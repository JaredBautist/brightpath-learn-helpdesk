export type Source = { docId: string; title: string; file: string; quote: string };
export type Success = { ok: true; provider: "nvidia" | "mock"; answerable: boolean; answer: string; sources: Source[] };
export type Failure = { ok: false; errorType: string; message: string };
export type AskResult = Success | Failure;

function isSource(value: unknown): value is Source {
  if (!value || typeof value !== "object") return false;
  return ["docId", "title", "file", "quote"].every(key => typeof Reflect.get(value, key) === "string");
}

function isResult(value: unknown): value is AskResult {
  if (!value || typeof value !== "object" || !("ok" in value)) return false;
  if (value.ok === false) return "errorType" in value && typeof value.errorType === "string" && "message" in value && typeof value.message === "string";
  return value.ok === true && "provider" in value && (value.provider === "mock" || value.provider === "nvidia") && "answerable" in value && typeof value.answerable === "boolean" && "answer" in value && typeof value.answer === "string" && "sources" in value && Array.isArray(value.sources) && value.sources.every(isSource);
}

/** Send one question; turn transport and malformed-response failures into displayable errors. */
export async function askQuestion(question: string, simulate: boolean): Promise<AskResult> {
  let response: Response;
  try {
    response = await fetch(`/api/ask${simulate ? "?simulate=failure" : ""}`, {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question }),
      signal: AbortSignal.timeout(75_000),
    });
  } catch {
    return { ok: false, errorType: "BACKEND_UNREACHABLE", message: "Cannot reach the backend. Is it running on port 8000?" };
  }
  try {
    const result: unknown = await response.json();
    if (isResult(result) && (response.ok || !result.ok)) return result;
  } catch {
    // A failed Next.js upstream proxy may return text instead of Django JSON.
  }
  return { ok: false, errorType: "BACKEND_UNREACHABLE", message: "Cannot reach the backend. Is it running on port 8000?" };
}
