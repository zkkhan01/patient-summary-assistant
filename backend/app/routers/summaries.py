from fastapi import APIRouter

from ..schemas import SummaryRequest, SummaryResponse
from ..pipeline import generate_summary

router = APIRouter(prefix="/summaries", tags=["summaries"])


@router.post("", response_model=SummaryResponse)
async def create_summary(payload: SummaryRequest) -> SummaryResponse:
    return generate_summary(
        patient_id=payload.patient_id,
        specialist=payload.specialist,
    )
