import httpx
from fastapi import HTTPException
from loguru import logger
from starlette import status


async def get_httpx_client():
    async with httpx.AsyncClient() as client:
        yield client


async def get_new_questions(count: int, httpx_client: httpx.AsyncClient) -> list:
    try:
        logger.info(f"Попытка получения новых вопросов от jservice.io, count={count}")
        response = await httpx_client.get(
            f'https://jservice.io/api/random?count={count}'
        )
        if response.status_code == 200:
            logger.info(f"Запрос к jservice.io выполнен успешно")
            return response.json()
        else:
            logger.warning(
                f"Не удалось получить данные от jservice.io. "
                f"Status: {response.status_code}, response: {response}"
            )
    except httpx.TimeoutException:
        pass
    except httpx.ConnectError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Question service is temporary unavailable"
        )
    return []


