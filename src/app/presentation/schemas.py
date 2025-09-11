import datetime

from pydantic import BaseModel, Field


class BirthdaySchema(BaseModel):
    owner: str = Field(..., min_length=1, max_length=50)
    date: datetime.date
