from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base

class Diary(Base):
    __tablename__ = "diary"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date,nullable=False)
    main_text = Column(String(2048))
    diary_img = Column(String(1024))
    
    user = relationship("User", back_populates="diaries")