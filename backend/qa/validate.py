import json
import re
from typing import TypedDict
from qa.docs import DOCUMENTS
from qa.errors import AppError

class Source(TypedDict):
    docId: str
    title: str
    file: str
    quote: str

class Answer(TypedDict):
    answerable: bool
    answer: str
    sources: list[Source]

UNAVAILABLE = "The information is not available in the supplied documents."
RESTRICTED = re.compile(r"\b(cost|price|pricing|refund|placement|precio|cuesta|costo|reembolso|empleo)\b", re.I)

def unavailable(question: str = "") -> Answer:
    """Return the canonical abstention, with a support referral where required."""
    answer = UNAVAILABLE
    if RESTRICTED.search(question):
        answer += " Please contact support@brightpath.example."
    return {"answerable": False, "answer": answer, "sources": []}

def normalize(value: str) -> str:
    return " ".join(value.casefold().split())

def validate(raw: str, question: str = "") -> Answer:
    """Parse model JSON and verify quote provenance; raise INVALID_MODEL_OUTPUT on schema errors."""
    cleaned = re.sub(r"^```(?:json)?\s*([\s\S]*?)\s*```$", r"\1", raw.strip(), flags=re.I)
    try:
        payload = json.loads(cleaned)
    except (ValueError, TypeError) as exc:
        raise AppError("INVALID_MODEL_OUTPUT") from exc
    if not isinstance(payload, dict) or type(payload.get("answerable")) is not bool or not isinstance(payload.get("answer"), str) or not payload["answer"].strip() or not isinstance(payload.get("sources"), list):
        raise AppError("INVALID_MODEL_OUTPUT")
    sources: list[Source] = []
    for source in payload["sources"]:
        if not isinstance(source, dict) or not isinstance(source.get("docId"), str) or not isinstance(source.get("quote"), str):
            raise AppError("INVALID_MODEL_OUTPUT")
        document = DOCUMENTS.get(source["docId"])
        quote = source["quote"].strip()
        if document and quote and normalize(quote) in normalize(document.text):
            sources.append({"docId": document.doc_id, "title": document.title, "file": document.file, "quote": quote})
    if not payload["answerable"] or not sources:
        return unavailable(question)
    return {"answerable": True, "answer": payload["answer"].strip(), "sources": sources}
