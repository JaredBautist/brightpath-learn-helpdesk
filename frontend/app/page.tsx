"use client";

import { useState, type FormEvent } from "react";
import { askQuestion, type AskResult } from "../lib/api";
import { AnswerResult } from "../components/help/AnswerResult";
import { HelpHeader } from "../components/help/HelpHeader";

export default function Home() {
  const [question, setQuestion] = useState("");
  const [simulate, setSimulate] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<AskResult | null>(null);
  const [provider, setProvider] = useState<"mock" | "nvidia" | null>(null);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (loading || !question.trim()) return;
    setLoading(true);
    setResult(null);
    const response = await askQuestion(question.trim(), simulate);
    if (response.ok) setProvider(response.provider);
    setResult(response);
    setLoading(false);
  }

  return (
    <main>
      <HelpHeader />
      <div className="workspace-meta">
        <span className="workspace-label">Your learning companion</span>
        {provider && <span className={`badge ${provider === "mock" ? "badge-mock" : ""}`}>Provider: {provider}</span>}
      </div>
      {provider === "mock" && (
        <p className="notice" role="status">
          <strong>Mock mode.</strong> This is a keyword-matching demo, not an AI model.
          It does not prove AI answer quality. Use English questions.
        </p>
      )}
      <form onSubmit={submit} aria-busy={loading}>
        <div className="field-heading">
          <label htmlFor="question">What would you like to know?</label>
          <span id="question-count" className="character-count">{question.length}/500</span>
        </div>
        <textarea
          id="question"
          value={question}
          onChange={event => setQuestion(event.target.value)}
          maxLength={500}
          rows={4}
          required
          disabled={loading}
          aria-describedby="question-hint question-count"
          placeholder="For example, where can I find the coaching link?"
        />
        <p id="question-hint" className="field-hint">Answers are based on the BrightPath Learn guides.</p>
        <div className="actions">
          <label className="checkbox">
            <input type="checkbox" checked={simulate} onChange={event => setSimulate(event.target.checked)} disabled={loading} />
            Simulate API failure
          </label>
          <button type="submit" disabled={loading || !question.trim()}>
            <span>{loading ? "Asking…" : "Ask question"}</span>
            <svg aria-hidden="true" viewBox="0 0 20 20" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
              <path d="M4 10h12m-5-5 5 5-5 5" />
            </svg>
          </button>
        </div>
      </form>
      <section className="response-region" aria-label="Question response" aria-live="polite" aria-atomic="true">
        {loading && (
          <div className="loading-state" role="status">
            <span className="loading-indicator" aria-hidden="true" />
            <div><strong>Checking your learning guides</strong><p>We’re looking for information that supports your answer.</p></div>
          </div>
        )}
        {result && <AnswerResult result={result} />}
      </section>
      <footer>
        <p>Grounded in your guides. Sources included.</p>
        <p className="footer-disclosure">A fictional BrightPath Learn project. Quotes show provenance; review the sources for context.</p>
      </footer>
    </main>
  );
}
