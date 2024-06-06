import datetime

from pydantic import BaseModel, Field


class DiaryBase(BaseModel):
    date: datetime.date | None = Field(None, example="2024-12-01")
    main_text: str = Field(..., example="今日も良い一日だった。")
    


class DiaryCreate(DiaryBase):
    pass


class DiaryCreateResponse(DiaryCreate):
    id: int
    user_id: int
    diary_img: str | None = Field(
        None,
        example="/static/images/2024-02-19T13:26:57.766065_643fbb.png",
    )

    class Config:
        orm_mode = True
    
class DiaryApiUpdate(BaseModel):
    date: datetime.date | None
    main_text: str | None
    

class DiaryDBUpdate(DiaryApiUpdate):
    diary_img: str | None

