from pydantic import BaseModel


class DoingResponse(BaseModel):
    id: int

    class Config:
        orm_mode = True
