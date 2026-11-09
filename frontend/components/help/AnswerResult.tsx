import type { AskResult } from "../../lib/api";

export function AnswerResult({ result }: { result: AskResult }) {
  if (!result.ok) {
    return (
      <div className="result error" role="alert">
        <div className="result-heading">
          <h2>Unable to answer</h2>
          <span className="error-code">{result.errorType}</span>
        </div>
        <p>{result.message}</p>
      </div>
    );
  }

  return (
    <article className={`result ${result.answerable ? "" : "not-found"}`}>
      <p className="eyebrow result-eyebrow">{result.answerable ? "From your learning guides" : "More information needed"}</p>
      <h2>{result.answerable ? "Your answer" : "Not found in the documents"}</h2>
      <p className="answer">{result.answer}</p>
      {result.sources.length > 0 && (
        <section className="source-section" aria-label="Supporting sources">
          <div className="sources-heading">
            <h3>Sources</h3>
            <span>From the supplied documents</span>
          </div>
          <ul className="sources">
            {result.sources.map((source, index) => (
              <li key={`${source.docId}-${index}`}>
                <div className="source-title">
                  <span className="document-label">{source.docId}</span>
                  <strong>{source.title}</strong>
                </div>
                <span className="filename">{source.file}</span>
                <blockquote>{source.quote}</blockquote>
              </li>
            ))}
          </ul>
        </section>
      )}
    </article>
  );
}
