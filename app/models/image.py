from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.session  import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    camera_id = Column(Integer, ForeignKey("cameras.id"), nullable=False)
    file_path = Column(String(255), nullable=False)
    captured_at = Column(DateTime, default=datetime.utcnow)
    extra_metadata = Column(JSON, nullable=True)  # <- antes se llamaba metadata

    camera = relationship("Camera", back_populates="images")
