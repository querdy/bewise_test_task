from fastapi import APIRouter

from app.api.endpoint import question


api_router = APIRouter()
api_router.include_router(question.router)
