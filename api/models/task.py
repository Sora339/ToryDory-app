from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    title = Column(String(1024), nullable=False)
    due_date = Column(Date)
    importance = Column(String(16), nullable=False)
    img_path = Column(String(1024))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    user = relationship("User", back_populates="tasks")
    doing = relationship("Doing", back_populates="task", cascade="delete")
    done = relationship("Done", back_populates="task", cascade="delete")

class Doing(Base):
    __tablename__ = "doings"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)

    task = relationship("Task", back_populates="doing")

class Done(Base):
    __tablename__ = "dones"

    id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    done_date = Column(Date, nullable=False)
    done_comment = Column(String(1024))

    task = relationship("Task", back_populates="done")


    
    
