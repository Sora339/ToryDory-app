import datetime
from pydantic import BaseModel


class DoneResponse(BaseModel):
    id: int
    done_date: datetime.date | None

    class Config:
        orm_mode = True
