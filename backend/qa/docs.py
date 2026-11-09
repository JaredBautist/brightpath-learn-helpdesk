from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Document:
    doc_id: str
    title: str
    file: str
    text: str


def load_documents() -> dict[str, Document]:
    """Load the fixed, public fictional corpus; raise OSError if missing."""
    documents = {}
    for index, path in enumerate(sorted((Path(__file__).resolve().parent.parent / "docs").glob("*.md")), 1):
        heading, body = path.read_text(encoding="utf-8").split("\n", 1)
        doc_id = f"DOC{index}"
        documents[doc_id] = Document(doc_id, heading.lstrip("# "), path.name, body.strip())
    if len(documents) != 3:
        raise RuntimeError("Expected the three supplied documents")
    return documents

DOCUMENTS = load_documents()
