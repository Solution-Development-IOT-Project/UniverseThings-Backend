from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class AutomationRule(Base):
    __tablename__ = "automation_rules"

    id = Column(Integer, primary_key=True, index=True)

    # Nombre de la regla
    name = Column(String(150), nullable=False)

    # Estado: ¿la regla está habilitada?
    is_active = Column(Boolean, default=True)

    # Prioridad:
    # 1 = máxima prioridad (se ejecuta primero)
    priority = Column(Integer, nullable=False, default=1)

    # Lógica de condición:
    # Representada en formato texto/JSON
    # Ejemplo:
    # {"sensor_id": 3, "operator": ">", "value": 30}
    condition = Column(Text, nullable=False)

    # Acción (opcional si deseas guardar algo más)
    # Usualmente se maneja con rule_actuator_map.
    action_description = Column(Text, nullable=True)

    zone_id = Column(Integer, ForeignKey("cultivation_zones.id", ondelete="CASCADE"), nullable=False)

    zone = relationship("CultivationZone", back_populates="automation_rules")


    actuators = relationship(
        "RuleActuatorMap",
        back_populates="rule",
        cascade="all, delete-orphan"
    )

    logs = relationship(
        "AutomationLog",
        back_populates="rule",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
