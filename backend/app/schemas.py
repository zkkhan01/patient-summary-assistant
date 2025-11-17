from datetime import datetime
from typing import Literal, List
from pydantic import BaseModel


SpecialistType = Literal[
    "primary_care",
    "cardiology",
    "dermatology",
    "endocrinology",
    "oncology",
]


class UploadDocumentRequest(BaseModel):
    patient_id: str
    doc_type: str


class UploadDocumentResponse(BaseModel):
    document_id: str
    patient_id: str
    stored_path: str


class SummaryRequest(BaseModel):
    patient_id: str
    specialist: SpecialistType


class Citation(BaseModel):
    document_id: str
    snippet: str
    location_hint: str


class SummaryResponse(BaseModel):
    patient_id: str
    specialist: SpecialistType
    generated_at: datetime
    text: str
    citations: List[Citation]
