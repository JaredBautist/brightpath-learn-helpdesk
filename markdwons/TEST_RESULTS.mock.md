# Acceptance test results

Generated: 2026-11-09T03:16:55.404390+00:00
Provider: **mock**
Transport: Django test Client (no browser or hosted deployment).

**Mock results do not prove AI answer quality.**

## Answerable: PASS

Question: How often is the group coaching session and where do I find the link?
Provider: mock
HTTP: 200
Why: Expected Tuesday 16:00 UTC and link 30 minutes before, with DOC2 evidence.

```json
{
  "ok": true,
  "provider": "mock",
  "answerable": true,
  "answer": "A group coaching session takes place every Tuesday at 16:00 UTC. The link appears on the Coaching page 30 minutes before the session.",
  "sources": [
    {
      "docId": "DOC2",
      "title": "Coaching and feedback",
      "file": "02-coaching-and-feedback.md",
      "quote": "A group coaching session takes place every Tuesday at 16:00 UTC."
    },
    {
      "docId": "DOC2",
      "title": "Coaching and feedback",
      "file": "02-coaching-and-feedback.md",
      "quote": "The link appears on the Coaching page 30 minutes before the session."
    }
  ]
}
```

## Not answerable: PASS

Question: How much does BrightPath Learn cost and can I get a refund?
Provider: mock
HTTP: 200
Why: Expected abstention, support referral, no invented numbers and no citations.

```json
{
  "ok": true,
  "provider": "mock",
  "answerable": false,
  "answer": "The information is not available in the supplied documents. Please contact support@brightpath.example.",
  "sources": []
}
```

## API failure: PASS

Question: When is coaching?
Provider: mock
HTTP: 503
Why: Expected a clear MODEL_UNAVAILABLE failure and no answer.

```json
{
  "ok": false,
  "errorType": "MODEL_UNAVAILABLE",
  "message": "The model is unavailable. Please try again later."
}
```

## Lesson completion: PASS

Question: Does watching the video mark the lesson complete?
Provider: mock
HTTP: 200
Why: Expected explicit lesson completion, not video-only completion, with DOC1 evidence.

```json
{
  "ok": true,
  "provider": "mock",
  "answerable": true,
  "answer": "Watching a video alone does not mark the lesson complete. To save your progress, select Mark complete after finishing a lesson.",
  "sources": [
    {
      "docId": "DOC1",
      "title": "Getting started",
      "file": "01-getting-started.md",
      "quote": "Watching a video alone does not mark the lesson complete."
    },
    {
      "docId": "DOC1",
      "title": "Getting started",
      "file": "01-getting-started.md",
      "quote": "To save your progress, select Mark complete after finishing a lesson."
    }
  ]
}
```
