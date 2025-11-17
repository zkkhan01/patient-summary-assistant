from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List

from .schemas import Citation, SummaryResponse, SpecialistType


@dataclass
class PatientDocument:
    id: str
    patient_id: str
    uploaded_at: datetime
    doc_type: str
    content: str
    source_filename: str


class InMemoryStore:
    def __init__(self) -> None:
        self.docs: Dict[str, PatientDocument] = {}

    def add(self, doc: PatientDocument) -> None:
        self.docs[doc.id] = doc

    def for_patient(self, patient_id: str) -> List[PatientDocument]:
        return [d for d in self.docs.values() if d.patient_id == patient_id]


store = InMemoryStore()


def add_document(patient_id: str, doc_type: str, content: str, filename: str) -> PatientDocument:
    doc = PatientDocument(
        id=str(uuid.uuid4()),
        patient_id=patient_id,
        uploaded_at=datetime.utcnow(),
        doc_type=doc_type,
        content=content,
        source_filename=filename,
    )
    store.add(doc)
    return doc


def generate_summary(patient_id: str, specialist: SpecialistType) -> SummaryResponse:
    docs = sorted(store.for_patient(patient_id), key=lambda d: d.uploaded_at)
    citations: List[Citation] = []
    bullets: List[str] = []

    for i, doc in enumerate(docs):
        snippet = doc.content[:260].replace("\n", " ")
        bullets.append(f"- {doc.doc_type.title()}: {snippet}")
        citations.append(
            Citation(
                document_id=doc.id,
                snippet=snippet,
                location_hint=f"{doc.source_filename}, section {i + 1}",
            )
        )

    if not bullets:
        summary_text = "No records available for this patient in the demo store."
    else:
        summary_text = (
            f"Specialist: {specialist}\n"
            f"Patient: {patient_id}\n\n"
            "Key information:\n"
            + "\n".join(bullets)
        )

    return SummaryResponse(
        patient_id=patient_id,
        specialist=specialist,
        generated_at=datetime.utcnow(),
        text=summary_text,
        citations=citations,
    )
