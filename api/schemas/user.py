from pydantic import BaseModel, Field


class UserBase(BaseModel):
    email: str = Field(..., example="a8199001@aoyama.jp")
    nickname: str | None = Field(None, example="tarou")


class UserCreate(UserBase):
    password: str = Field(..., example="1234")


class UserDBUpdate(BaseModel):
    icon_img: str | None
    
class UserResponse(UserBase):
    id: int
    icon_img: str | None = Field(
       None,
       example="/static/images/2024-02-19T13:26:57.766065_643fbb.png",
    )

    class Config:
        orm_mode = True
