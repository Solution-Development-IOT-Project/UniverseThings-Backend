from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Sensor(Base):
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    sensor_type = Column(String(100), nullable=False)       # Ej: temp, humedad, ph, ndvi
    model = Column(String(100), nullable=True)              # Modelo del sensor físico
    unit = Column(String(50), nullable=True)                # °C, %, pH, NDVI…

    is_active = Column(Boolean, default=True)

    zone_id = Column(
        Integer,
        ForeignKey("cultivation_zones.id", ondelete="CASCADE"),
        nullable=False,
    )

    # ----------------- RELACIONES -----------------

    # Zona a la que pertenece
    zone = relationship("CultivationZone", back_populates="sensors")

    # Mediciones del sensor
    measurements = relationship(
        "Measurement",
        back_populates="sensor",
        cascade="all, delete-orphan",
    )

    # 🔹 ESTA ES LA RELACIÓN QUE FALTABA
    threshold_configs = relationship(
        "ThresholdConfig",
        back_populates="sensor",
        cascade="all, delete-orphan",
    )

    # ----------------------------------------------

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
