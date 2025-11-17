import os
from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from datetime import datetime

from ..schemas import UploadDocumentRequest, UploadDocumentResponse
from ..pipeline import add_document

router = APIRouter(prefix="/patients", tags=["patients"])


@router.post("/{patient_id}/documents", response_model=UploadDocumentResponse)
async def upload_document(
    patient_id: str,
    payload: UploadDocumentRequest,
    file: Annotated[UploadFile, File(...)],
):
    raw_bytes = await file.read()
    try:
        content = raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        content = "<binary or scanned content - route through PaddleOCR in production>"

    os.makedirs("data/uploads", exist_ok=True)
    stored_path = os.path.join("data", "uploads", f"{datetime.utcnow().timestamp()}_{file.filename}")
    with open(stored_path, "wb") as f:
        f.write(raw_bytes)

    doc = add_document(
        patient_id=patient_id,
        doc_type=payload.doc_type,
        content=content,
        filename=file.filename,
    )

    return UploadDocumentResponse(
        document_id=doc.id,
        patient_id=patient_id,
        stored_path=stored_path,
    )
