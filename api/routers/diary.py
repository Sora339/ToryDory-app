from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

import api.cruds.diary as diary_crud
import api.schemas.diary as diary_schema
from api.db import get_db
from api.extra_modules.auth.core import get_current_user
from api.extra_modules.image.core import save_image
from api.models.user import User as UserModel

router = APIRouter()


@router.post("/diary", response_model=diary_schema.DiaryCreateResponse)
def create_diary(
    diary_body: diary_schema.DiaryCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return diary_crud.create_diary(db, diary_body, current_user.id)


@router.get("/diarys", response_model=list[diary_schema.DiaryCreateResponse])
def list_diarys(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    return diary_crud.get_multiple_diarys_with_done(db, current_user.id)

@router.get("/diary/{diary_id}", response_model=diary_schema.DiaryCreateResponse)
def get_task(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    diary = diary_crud.get_diary_with_done(db, diary_id=diary_id)

    # タスクが存在しない場合
    if diary is None:
        raise HTTPException(status_code=404, detail="Diary not found")

    diary = diary_schema.DiaryCreateResponse.from_orm(diary)
    # 他のユーザーのタスクを取得しようとした場合
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return diary


@router.put("/diary/{diary_id}", response_model=diary_schema.DiaryCreateResponse)
def update_diary(
    diary_id: int,
    diary_body: diary_schema.DiaryApiUpdate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    diary = diary_crud.get_diary(db, diary_id=diary_id)

    # タスクが存在しない場合
    if diary is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # 他のユーザーのタスクを変更しようとした場合
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return diary_crud.update_diary(
        db,
        diary_schema.DiaryDBUpdate(**diary_body.dict()),
        original=diary,
    )
    
@router.put(
    "/diary/{diary_id}/image",
    response_model=diary_schema.DiaryCreateResponse,
)
def add_image_to_diary(
    diary_id: int,
    diary_img_path: UploadFile,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    diary = diary_crud.get_diary(db, diary_id=diary_id)

    # タスクが存在しない場合
    if diary is None:
        raise HTTPException(status_code=404, detail="Diary not found")
    #  他のユーザーのタスクを変更しようとした場合
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    diary_img = save_image(diary_img_path)

    return diary_crud.update_diary(
        db,
        diary_schema.DiaryDBUpdate(diary_img=diary_img),
        original=diary,
    )


@router.delete("/diary/{diary_id}", response_model=None)
def delete_diary(
    diary_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    diary = diary_crud.get_diary(db, diary_id=diary_id)

    # タスクが存在しない場合
    if diary is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # 他のユーザーのタスクを削除しようとした場合
    if diary.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return diary_crud.delete_diary(db, original=diary)