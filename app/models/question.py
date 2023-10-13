import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import mapped_column, Mapped

from app.database.db import Base


class Question(Base):
    __tablename__ = "question"

    question_id: Mapped[int] = mapped_column(unique=True)
    text: Mapped[str] = mapped_column()
    answer: Mapped[str] = mapped_column()
    created_at: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=True))

