from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

import api.models.task as task_model


def get_doing(db: Session, task_id: int) -> task_model.Doing | None:
    result: Result = db.execute(
        select(task_model.Doing).filter(task_model.Doing.id == task_id)
    )
    return result.scalars().first()


def create_doing(db: Session, task_id: int) -> task_model.Doing:
    doing = task_model.Doing(id=task_id)
    db.add(doing)
    db.commit()
    db.refresh(doing)
    return doing


def delete_doing(db: Session, original: task_model.Doing) -> None:
    db.delete(original)
    db.commit()
