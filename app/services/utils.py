import asyncio

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.crud.question import get_non_unique_questions_ids
from app.services.jservice_io import get_new_questions


async def collect_unique_questions(question_count: int, httpx_client: AsyncClient, db: AsyncSession) -> list:
    unique_questions = []
    while True:
        new_questions = await collect_questions(
            question_count=question_count - len(unique_questions),
            httpx_client=httpx_client
        )
        db_question_ids = await get_non_unique_questions_ids(
            db=db,
            question_ids=[question.get("id") for question in new_questions],
        )
        unique_questions_ids = [question.get("id") for question in unique_questions]
        unique_questions.extend(
            [
                question for question in new_questions
                if (question.get("id") not in db_question_ids
                    and question.get("id") not in unique_questions_ids)
            ]
        )
        if not db_question_ids and len(unique_questions) == question_count:
            break
    return unique_questions


async def collect_questions(question_count: int, httpx_client: AsyncClient):
    api_max_count = 100
    pending = []
    new_questions = []
    for count in range(question_count // api_max_count + 1):
        pending.append(asyncio.create_task(
            get_new_questions(
                api_max_count if count < question_count // api_max_count else question_count % api_max_count,
                httpx_client=httpx_client
            )
        ))
    done, pending = await asyncio.wait(
        pending, return_when=asyncio.ALL_COMPLETED
    )
    for task in done:
        new_questions_ids = [question.get("id") for question in new_questions]
        result = task.result()
        new_questions.extend(
            [question for question in result
             if question.get("id") not in new_questions_ids]
        )
    return new_questions
