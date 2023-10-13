import sys

from fastapi import FastAPI
from loguru import logger
from starlette.middleware.cors import CORSMiddleware

from app.api.router import api_router

from app.settings import settings

logger.remove()
logger.add(sys.stderr, level="INFO")

app = FastAPI(
    title="Bewise.ai test task",
    docs_url=f"{settings.API_STR}/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_STR)
