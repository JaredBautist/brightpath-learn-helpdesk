import json
import re
from qa.docs import DOCUMENTS
from qa.validate import RESTRICTED, unavailable

STOPWORDS = set("a an the is are do does how where when what and or to of in on for i it my can get find often much brightpath learn session".split())

def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS

class MockProvider:
    """English lexical demo. Not a model and not evidence of AI quality."""
    def generate(self, system: str, user: str) -> str:
        if RESTRICTED.search(user):
            return json.dumps(unavailable(user))
        question_tokens = tokens(user)
        candidates = []
        for document in DOCUMENTS.values():
            for sentence in re.split(r"(?<=[.!?])\s+", document.text):
                score = len(question_tokens & tokens(sentence))
                if score >= 2:
                    candidates.append((score, document.doc_id, sentence))
        candidates.sort(key=lambda candidate: candidate[0], reverse=True)
        if not candidates:
            return json.dumps(unavailable(user))
        selected = candidates[:2]
        # Keep the feedback timing caveat even when sentence ranking omits it.
        answer = " ".join(sentence for _, _, sentence in selected)
        if "Feedback usually" in answer:
            answer += " This is a typical response time, not a guarantee."
        return json.dumps({"answerable": True, "answer": answer, "sources": [{"docId": doc_id, "quote": sentence} for _, doc_id, sentence in selected]})
