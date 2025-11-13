from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Camera(Base):
    __tablename__ = "cameras"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)                  # Ej: "Cam NDVI Zona 1"
    camera_type = Column(String(100), nullable=False)           # RGB, NDVI, thermal, multispectral
    model = Column(String(100), nullable=True)                  # Modelo específico

    is_active = Column(Boolean, default=True)

    location_description = Column(String(255), nullable=True)

    zone_id = Column(Integer, ForeignKey("cultivation_zones.id", ondelete="CASCADE"), nullable=False)

    zone = relationship("CultivationZone", back_populates="cameras")

    images = relationship(
        "Image",
        back_populates="camera",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
