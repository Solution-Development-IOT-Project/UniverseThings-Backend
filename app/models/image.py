from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)

    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)

    file_path = Column(String(255), nullable=False)

    # campos que tu API ya expone
    image_type = Column(String(50), nullable=False)      # "rgb", "ndvi", etc.

    # 👇 atributo Python = image_metadata, nombre de columna en BD = metadata
    image_metadata = Column("metadata", JSON, nullable=True)

    analysis_result = Column(Text, nullable=True)

    captured_at = Column(DateTime(timezone=True), server_default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    camera = relationship("Camera", back_populates="images")
