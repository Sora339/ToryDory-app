from sqlalchemy import select
from sqlalchemy.engine import Result ,Row
from sqlalchemy.orm import Session

import api.models.task as task_model
import api.schemas.done as done_schema


def get_done(db: Session, task_id: int) -> task_model.Done | None:
    result: Result = db.execute(
        select(task_model.Done).filter(task_model.Done.id == task_id)
    )
    return result.scalars().first()


def create_done(
    db: Session,
    done_date: done_schema.DoneCreate,
    task_id: int
    ) -> task_model.Done:
    done = task_model.Done(id=task_id, done_date=done_date.done_date)
    db.add(done)
    db.commit()
    db.refresh(done)
    return done


def delete_done(db: Session, original: task_model.Done) -> None:
    db.delete(original)
    db.commit()
    
# def get_multiple_donetasks(
#     db: Session,
#     user_id: int,
# ) -> list[Row]:
#     result: Result = db.execute(
#         select(
#             task_model.Done.id,
#             task_model.Done.done_date,
#         )
#         .filter(task_model.Task.user_id == user_id)
#     )

#     return result.all()

def get_multiple_donetasks(
    db: Session,
    user_id: int,
) -> list[Row]:
    result: Result = db.execute(
        select(
            task_model.Done.id,
            task_model.Done.done_date,
        )
        .join(task_model.Task, task_model.Done.id == task_model.Task.id)  # 明示的な結合
        .filter(task_model.Task.user_id == user_id)
    )

    return result.all()