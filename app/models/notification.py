from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    # Título corto de la notificación
    title = Column(String(200), nullable=False)

    # Contenido detallado
    message = Column(Text, nullable=False)

    # Tipo de notificación:
    # alert, automation, report, device, system
    notification_type = Column(String(50), nullable=False, default="alert")

    # Estado de lectura
    is_read = Column(Boolean, default=False)

    # Canal por donde se envió (opcional)
    # Ej: push, email, sms, internal
    channel = Column(String(50), nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    user = relationship("User", backref="notifications")

    alert_id = Column(
        Integer,
        ForeignKey("alerts.id", ondelete="SET NULL"),
        nullable=True
    )

    alert = relationship("Alert", backref="notifications")

    sensor_id = Column(
        Integer,
        ForeignKey("sensors.id", ondelete="SET NULL"),
        nullable=True
    )

    sensor = relationship("Sensor", backref="notifications")


    actuator_id = Column(
        Integer,
        ForeignKey("actuators.id", ondelete="SET NULL"),
        nullable=True
    )

    actuator = relationship("Actuator", backref="notifications")

    zone_id = Column(
        Integer,
        ForeignKey("cultivation_zones.id", ondelete="SET NULL"),
        nullable=True
    )

    zone = relationship("CultivationZone", backref="notifications")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    read_at = Column(DateTime(timezone=True), nullable=True)

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
