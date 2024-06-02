import datetime
from pydantic import BaseModel, Field

class DoneBase(BaseModel):
    done_date: datetime.date | None = Field(None, example="2024-12-01")
    
class DoneCreate(DoneBase):
    pass

class DoneResponse(DoneCreate):
    id: int

    class Config:
        orm_mode = True
