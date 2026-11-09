# Hosted verification results

Checked: 2026-11-09T04:58:06.421227+00:00

Frontend/proxy: https://brightpath-learn-helpdesk.vercel.app
Backend: https://brightpath-api-l80c.onrender.com
Code: https://github.com/JaredBautist/brightpath-learn-helpdesk

Unauthenticated checks confirmed the frontend and repository return HTTP 200. POST checks below used the Vercel `/api/ask` rewrite, not a direct Django test Client. The developer also supplied a screenshot of a successful coaching answer in the deployed UI with the NVIDIA badge.

## Supported question — first attempt

HTTP: 504

```json
{
  "ok": false,
  "errorType": "TIMEOUT",
  "message": "The model did not respond within 15 seconds. Please try again."
}
```

## Unknown information

HTTP: 200

```json
{
  "ok": true,
  "provider": "nvidia",
  "answerable": false,
  "answer": "The information is not available in the supplied documents. Please contact support@brightpath.example.",
  "sources": []
}
```

## Simulated API failure

HTTP: 503

```json
{
  "ok": false,
  "errorType": "MODEL_UNAVAILABLE",
  "message": "The model is unavailable. Please try again later."
}
```

## Supported question — retry

HTTP: 200

```json
{
  "ok": true,
  "provider": "nvidia",
  "answerable": true,
  "answer": "The group coaching session takes place every Tuesday at 16:00 UTC. The link appears on the Coaching page 30 minutes before the session.",
  "sources": [
    {
      "docId": "DOC2",
      "title": "Coaching and feedback",
      "file": "02-coaching-and-feedback.md",
      "quote": "A group coaching session takes place every Tuesday at 16:00 UTC. The link appears on the Coaching page 30 minutes before the session."
    }
  ]
}
```

## Interpretation

The three required behaviors were observed through the hosted proxy: sourced NVIDIA answer on retry, correct abstention and simulated failure without an answer. The first supported request timed out (HTTP 504/TIMEOUT); the retry returned HTTP 200 with DOC2 evidence. Keep this intermittent model/transport latency limitation explicit. Simulation is deliberately handled before provider invocation.

This does not constitute an exhaustive browser, accessibility, fresh-clone or reliability evaluation. Deployment logs were not independently audited, and the earlier local build limitation is retained as historical evidence.
