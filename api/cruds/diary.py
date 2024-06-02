from sqlalchemy import select
from sqlalchemy.engine import Result, Row
from sqlalchemy.orm import Session

import api.models.diary as diary_model
import api.schemas.diary as diary_schema


def create_diary(
    db: Session,
    diary_create: diary_schema.DiaryCreate,
    user_id: int,
) -> diary_model.Diary:
    diary = diary_model.Diary(**diary_create.dict(), user_id=user_id)
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary


def get_diary(
    db: Session,
    diary_id: int,
) -> diary_model.Diary | None:
    result: Result = db.execute(
        select(diary_model.Diary).filter(diary_model.Diary.id == diary_id)
    )
    return result.scalars().first()


def get_diary_with_done(
    db: Session,
    diary_id: int,
) -> Row | None:
    result: Result = db.execute(
        select(
            diary_model.Diary.id,
            diary_model.Diary.main_text,
            diary_model.Diary.date,
            diary_model.Diary.user_id,
            diary_model.Diary.diary_img,
        )
        .filter(diary_model.Diary.id == diary_id)
    )
    return result.first()


def get_multiple_diarys_with_done(
    db: Session,
    user_id: int,
) -> list[Row]:
    result: Result = db.execute(
        select(
            diary_model.Diary.id,
            diary_model.Diary.main_text,
            diary_model.Diary.date,
            diary_model.Diary.user_id,
            diary_model.Diary.diary_img,
        )
        .filter(diary_model.Diary.user_id == user_id)
    )
    return result.all()


def update_diary(
    db: Session,
    diary_create: diary_schema.DiaryDBUpdate,
    original: diary_model.Diary,
) -> diary_model.Diary:

    if diary_create.main_text is not None:
        original.main_text = diary_create.main_text

    if diary_create.diary_img is not None:
        original.diary_img = diary_create.diary_img

    db.add(original)
    db.commit()
    db.refresh(original)
    return original


def delete_task(db: Session, original: diary_model.Diary):
    db.delete(original)
    db.commit()
