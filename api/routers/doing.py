from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import api.cruds.doing as doing_crud
import api.cruds.task as task_crud
import api.schemas.doing as doing_schema
from api.db import get_db
from api.extra_modules.auth.core import get_current_user
from api.models.user import User as UserModel

router = APIRouter()


@router.put("/task/{task_id}/doing", response_model=doing_schema.DoingResponse)
def mark_task_as_doing(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    task = task_crud.get_task(db, task_id=task_id)
    # 存在した場合
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    # 違うユーザーのタスクを変更しようとした場合
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    doing = doing_crud.get_doing(db, task_id=task_id)
    # すでにdoingがされている場合
    if doing is not None:
        raise HTTPException(status_code=400, detail="Doing already exists")

    return doing_crud.create_doing(db, task_id)


@router.delete("/task/{task_id}/doing", response_model=None)
def unmark_task_as_doing(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):

    doing = doing_crud.get_doing(db, task_id=task_id)
    # doingリソースが存在しない場合
    if doing is None:
        raise HTTPException(status_code=404, detail="Not found")

    task = task_crud.get_task(db, task_id=task_id)
    # 違うユーザーのタスクを変更しようとした場合
    if task.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    return doing_crud.delete_doing(db, original=doing)
