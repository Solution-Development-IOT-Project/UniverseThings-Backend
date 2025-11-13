from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Alert(Base):
    __tablename__ = "alerts"


    id = Column(Integer, primary_key=True, index=True)

    # Mensaje principal de la alerta
    message = Column(String(255), nullable=False)

    # Descripción más detallada (opcional)
    details = Column(Text, nullable=True)

    # Severidad de la alerta
    # Ej: info, warning, critical
    severity = Column(String(50), nullable=False, default="info")

    # Estado: ¿el usuario ya la vio?
    is_read = Column(Boolean, default=False)


    sensor_id = Column(Integer, ForeignKey("sensors.id", ondelete="SET NULL"), nullable=True)

    sensor = relationship("Sensor", backref="alerts")


    zone_id = Column(Integer, ForeignKey("cultivation_zones.id", ondelete="CASCADE"), nullable=False)

    zone = relationship("CultivationZone", backref="alerts")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    resolved_at = Column(DateTime(timezone=True), nullable=True)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
