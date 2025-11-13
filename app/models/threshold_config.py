from sqlalchemy import Column, Integer, Float, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class ThresholdConfig(Base):
    __tablename__ = "threshold_configs"

    id = Column(Integer, primary_key=True, index=True)

    # Tipo de variable monitoreada (temperature, humidity, ph, ndvi, etc.)
    parameter = Column(String(100), nullable=False)

    # Umbrales (pueden ser opcionales)
    min_value = Column(Float, nullable=True)          # límite inferior
    max_value = Column(Float, nullable=True)          # límite superior

    # Umbrales de advertencia (niveles intermedios)
    warn_min = Column(Float, nullable=True)
    warn_max = Column(Float, nullable=True)

    # Estado de la configuración
    is_active = Column(Boolean, default=True)

    # Operador de disparo:
    # >, <, >=, <=, between
    operator = Column(String(20), nullable=False, default="between")

    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False)

    sensor = relationship("Sensor", back_populates="threshold_configs")

    zone_id = Column(Integer, ForeignKey("cultivation_zones.id", ondelete="CASCADE"), nullable=False)

    zone = relationship("CultivationZone", back_populates="threshold_configs")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
