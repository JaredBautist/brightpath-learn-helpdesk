"""Run the take-home acceptance cases through Django, without a running server."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys

BACKEND = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()
from django.test import Client
from qa.service import select_provider
from qa.errors import AppError

CASES = [
    ("Answerable", "How often is the group coaching session and where do I find the link?"),
    ("Not answerable", "How much does BrightPath Learn cost and can I get a refund?"),
    ("API failure", "When is coaching?"),
    ("Lesson completion", "Does watching the video mark the lesson complete?"),
]

def check_case(name: str, status: int, payload: dict) -> tuple[bool, str]:
    """Check observable content and citations, not just success status."""
    answer = payload.get("answer", "").casefold()
    sources = payload.get("sources", [])
    if name == "API failure":
        passed = status == 503 and payload.get("ok") is False and payload.get("errorType") == "MODEL_UNAVAILABLE" and "answer" not in payload
        return passed, "Expected a clear MODEL_UNAVAILABLE failure and no answer."
    if not payload.get("ok") or status != 200:
        return False, "Expected a successful API response."
    if name == "Not answerable":
        passed = payload.get("answerable") is False and sources == [] and "not available in the supplied documents" in answer and "support@brightpath.example" in answer and not any(char.isdigit() for char in answer)
        return passed, "Expected abstention, support referral, no invented numbers and no citations."
    if name == "Answerable":
        evidence = " ".join(source.get("quote", "") for source in sources if source.get("docId") == "DOC2").casefold()
        passed = payload.get("answerable") is True and all(term in answer for term in ["tuesday", "16:00", "utc", "coaching page", "30 minutes"]) and all(term in evidence for term in ["tuesday", "16:00", "30 minutes"])
        return passed, "Expected Tuesday 16:00 UTC and link 30 minutes before, with DOC2 evidence."
    passed = payload.get("answerable") is True and "mark complete" in answer and ("does not" in answer or "no" in answer) and any(source.get("docId") == "DOC1" for source in sources)
    return passed, "Expected explicit lesson completion, not video-only completion, with DOC1 evidence."


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="Default: repository TEST_RESULTS[.mock].md based on selected provider")
    args = parser.parse_args()
    try:
        provider, _ = select_provider()
    except AppError:
        provider = os.getenv("LLM_PROVIDER", "nvidia")
    output = args.output or BACKEND.parent / ("TEST_RESULTS.mock.md" if provider == "mock" else "TEST_RESULTS.md")
    lines = ["# Acceptance test results", "", f"Generated: {datetime.now(timezone.utc).isoformat()}", f"Provider: **{provider}**", "Transport: Django test Client (no browser or hosted deployment).", ""]
    if provider == "mock":
        lines += ["**Mock results do not prove AI answer quality.**", ""]
    failed = 0
    client = Client()
    original = os.environ.get("SIMULATE_FAILURE")
    try:
        for name, question in CASES:
            os.environ["SIMULATE_FAILURE"] = "true" if name == "API failure" else "false"
            response = client.post("/api/ask", json.dumps({"question":question}), content_type="application/json")
            payload = response.json()
            passed, reason = check_case(name, response.status_code, payload)
            failed += not passed
            lines += [f"## {name}: {'PASS' if passed else 'FAIL'}", "", f"Question: {question}", f"Provider: {payload.get('provider', provider)}", f"HTTP: {response.status_code}", f"Why: {reason}", "", "```json", json.dumps(payload, indent=2), "```", ""]
    finally:
        if original is None:
            os.environ.pop("SIMULATE_FAILURE", None)
        else:
            os.environ["SIMULATE_FAILURE"] = original
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"{len(CASES) - failed}/{len(CASES)} cases passed; saved {output.name}")
    return int(failed > 0)

if __name__ == "__main__":
    raise SystemExit(main())
