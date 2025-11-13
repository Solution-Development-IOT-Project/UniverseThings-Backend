from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Actuator(Base):
    __tablename__ = "actuators"


    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)                  # Ej: "Válvula principal", "Bomba 1"
    actuator_type = Column(String(100), nullable=False)         # Ej: irrigation, fan, pump, light
    model = Column(String(100), nullable=True)                  # Modelo del actuador físico

    is_on = Column(Boolean, default=False)


    auto_mode = Column(Boolean, default=True)


    zone_id = Column(Integer, ForeignKey("cultivation_zones.id", ondelete="CASCADE"), nullable=False)

    zone = relationship("CultivationZone", back_populates="actuators")

    rule_links = relationship(
        "RuleActuatorMap",
        back_populates="actuator",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
