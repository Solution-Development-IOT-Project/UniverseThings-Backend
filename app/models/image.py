from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)

    # Ruta donde se almacena la imagen (S3, local, etc.)
    file_path = Column(String(255), nullable=False)

    # Ej: rgb, ndvi, thermal, segmentation, anomaly
    image_type = Column(String(50), nullable=False)

    metadata = Column(Text, nullable=True)

    # Resultado de análisis (opcional)
    # Ej: NDVI=0.67, análisis IA, etiquetas, bounding boxes
    analysis_result = Column(Text, nullable=True)

    camera_id = Column(Integer, ForeignKey("cameras.id", ondelete="CASCADE"), nullable=False)

    camera = relationship("Camera", back_populates="images")
