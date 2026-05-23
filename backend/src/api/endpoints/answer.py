"""AI answer endpoint."""

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.depends import AnswerServiceDependency
from src.api.depends import get_db
from src.api.schemas import AnswerRequest, AnswerResponse
from src.utils.logging.qa_audit import record_qa_pair


router = APIRouter(tags=["answer"])


@router.post("/answer", response_model=AnswerResponse)
async def answer_question(
    payload: AnswerRequest,
    answer_service: AnswerServiceDependency,
    session: AsyncSession = Depends(get_db),
) -> AnswerResponse:
    """Generate a transcript-backed AI answer for a user prompt."""

    message = await answer_service.answer(prompt=payload.prompt)
    await record_qa_pair(session=session, prompt=payload.prompt, answer=message)
    return AnswerResponse(message=message)
