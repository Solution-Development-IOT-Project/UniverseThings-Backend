from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Measurement(Base):
    __tablename__ = "measurements"


    id = Column(Integer, primary_key=True, index=True)

    value = Column(Float, nullable=False)

    unit = Column(String(20), nullable=True)

    status = Column(String(50), nullable=True)
    # Ejemplos:
    # "normal", "warning", "critical", "offline", etc.

    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)

    sensor = relationship("Sensor", back_populates="measurements")
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
