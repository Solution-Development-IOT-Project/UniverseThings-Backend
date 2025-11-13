from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class RuleActuatorMap(Base):
    __tablename__ = "rule_actuator_map"


    id = Column(Integer, primary_key=True, index=True)

    rule_id = Column(
        Integer,
        ForeignKey("automation_rules.id", ondelete="CASCADE"),
        nullable=False
    )

    rule = relationship("AutomationRule", back_populates="actuators")

    actuator_id = Column(
        Integer,
        ForeignKey("actuators.id", ondelete="CASCADE"),
        nullable=False
    )

    actuator = relationship("Actuator", back_populates="rule_links")


    # Estado deseado cuando la regla se dispara
    # Ej: True = encender, False = apagar
    desired_state = Column(Boolean, default=True)

    # Duración de la acción en segundos (opcional)
    # Ej: mantener válvula abierta 600s
    duration_seconds = Column(Integer, nullable=True)

    # Descripción opcional de la acción
    action_note = Column(String(255), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
