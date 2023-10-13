from typing import Sequence

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models
from app.api.schema.question import QuestionSchema


async def save_questions(db: AsyncSession, questions: list[QuestionSchema]) -> Sequence[models.Question]:
    saved_question = await db.scalars(
        insert(models.Question)
        .returning(models.Question),
        [question.model_dump() for question in questions]
    )
    await db.commit()
    return saved_question.all()


async def get_non_unique_questions_ids(db: AsyncSession, question_ids: list[int]) -> Sequence[int]:
    result = await db.scalars(
        select(models.Question.question_id)
        .where(models.Question.question_id.in_(question_ids))
    )
    return result.all()
