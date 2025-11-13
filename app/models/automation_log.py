from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class AutomationLog(Base):
    __tablename__ = "automation_logs"

    id = Column(Integer, primary_key=True, index=True)

    # Resultado de la ejecución
    # Ej: "triggered", "skipped", "failed"
    status = Column(String(50), nullable=False, default="triggered")

    # Mensaje corto
    message = Column(String(255), nullable=True)

    # Detalles extendidos (stacktrace, datos de sensores, etc.)
    details = Column(Text, nullable=True)

    # ¿La acción fue realmente ejecutada en el actuador?
    action_executed = Column(Boolean, default=False)

    rule_id = Column(
        Integer,
        ForeignKey("automation_rules.id", ondelete="CASCADE"),
        nullable=False
    )

    rule = relationship("AutomationRule", back_populates="logs")

    actuator_id = Column(
        Integer,
        ForeignKey("actuators.id", ondelete="SET NULL"),
        nullable=True
    )

    actuator = relationship("Actuator", backref="automation_logs")

    sensor_id = Column(
        Integer,
        ForeignKey("sensors.id", ondelete="SET NULL"),
        nullable=True
    )

    sensor = relationship("Sensor", backref="automation_logs")

    zone_id = Column(
        Integer,
        ForeignKey("cultivation_zones.id", ondelete="SET NULL"),
        nullable=True
    )

    zone = relationship("CultivationZone", backref="automation_logs")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
