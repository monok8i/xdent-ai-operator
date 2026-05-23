"""AI answer endpoint."""

from fastapi import APIRouter

from src.api.depends import AnswerServiceDependency
from src.api.schemas import AnswerRequest, AnswerResponse


router = APIRouter(tags=["answer"])


@router.post("/answer", response_model=AnswerResponse)
async def answer_question(
    payload: AnswerRequest,
    answer_service: AnswerServiceDependency,
) -> AnswerResponse:
    """Generate a transcript-backed AI answer for a user prompt."""

    message = await answer_service.answer(prompt=payload.prompt)
    return AnswerResponse(message=message)
