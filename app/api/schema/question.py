import datetime
import uuid

from pydantic import BaseModel, Field


class QuestionCountSchema(BaseModel):
    questions_num: int = Field(
        ge=0,
        # le=1000
        default=1
    )


class QuestionSchema(BaseModel):
    question_id: int
    text: str
    answer: str
    created_at: datetime.datetime


class ResponseQuestionSchema(QuestionSchema):
    uuid: uuid.UUID
