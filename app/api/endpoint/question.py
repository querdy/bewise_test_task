from fastapi import APIRouter, Depends, HTTPException
from httpx import AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.api.crud.question import save_questions
from app.api.schema.question import QuestionCountSchema, QuestionSchema, ResponseQuestionSchema
from app.database.db import get_session
from app.services.jservice_io import get_httpx_client
from app.services.utils import collect_unique_questions

router = APIRouter(prefix="/question", tags=["Question"])


@router.post("/", response_model=list[ResponseQuestionSchema], status_code=status.HTTP_201_CREATED)
async def get_new_questions_route(
        question_count: QuestionCountSchema,
        db: AsyncSession = Depends(get_session),
        httpx_client: AsyncClient = Depends(get_httpx_client),
):
    try:
        unique_questions = await collect_unique_questions(
            question_count.questions_num,
            httpx_client=httpx_client,
            db=db,
        )
        if not unique_questions:
            logger.warning(f"Не удалось получить новые уникальные вопросы. Запрошено: {question_count.questions_num}")
            return []
        saved_questions = await save_questions(
            db=db,
            questions=[QuestionSchema(
                question_id=question.get("id"),
                text=question.get("question"),
                answer=question.get("answer"),
                created_at=question.get("created_at"),
            ) for question in unique_questions])
        logger.info(f"В базу данных сохранено вопросов: {len(saved_questions)}")
        return saved_questions
    except Exception as e:
        logger.warning(f"{e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Service temporary unavailable"
        )


