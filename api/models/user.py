from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    nickname = Column(String(64))
    password = Column(String(64), nullable=False)
    icon_img = Column(String(1024))

    tasks = relationship("Task", back_populates="user", cascade="delete")
    diaries = relationship("Diary", back_populates="user", cascade="delete")
