from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

import api.cruds.user as user_crud
import api.schemas.user as user_schema
from api.db import get_db
from api.extra_modules.auth.core import get_current_user
from api.extra_modules.image.core import save_image
from api.models.user import User as UserModel

router = APIRouter()


@router.post("/user", response_model=user_schema.UserResponse)
def create_user(
    user: user_schema.UserCreate,
    db: Session = Depends(get_db),
):
    db_user = user_crud.get_user_by_email(db, email=user.email)
    # すでに登録されているメールアドレスの場合
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_crud.create_user(db, user)

@router.put(
    "/user/{user_id}/image",
    response_model=user_schema.UserResponse,
)
def add_image_to_user(
    user_id: int,
    icon_img_path: UploadFile,
    db: Session = Depends(get_db),
):
    
    user = user_crud.get_user(db, user_id=user_id)
    
    # ユーザーが存在しない場合
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    icon_img = save_image(icon_img_path)

    return user_crud.update_user(
        db,
        user_schema.UserDBUpdate(icon_img=icon_img),
        original=user,
    )


@router.get("/me", response_model=user_schema.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user
