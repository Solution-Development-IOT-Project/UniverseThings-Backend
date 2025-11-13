from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Device(Base):
    __tablename__ = "devices"

    id = Column(Integer, primary_key=True, index=True)

    # Nombre lógico del dispositivo
    name = Column(String(150), nullable=False)               # Ej: "Gateway Zona 1", "Nodo 3"

    # Tipo de dispositivo
    # Ej: gateway, controller, node, edge_computer, router
    device_type = Column(String(100), nullable=False)

    # Identificadores de hardware
    serial_number = Column(String(100), unique=True, nullable=True)
    firmware_version = Column(String(50), nullable=True)

    # Estado de conexión
    is_online = Column(Boolean, default=False)
    last_seen = Column(DateTime(timezone=True), nullable=True)


    zone_id = Column(
        Integer,
        ForeignKey("cultivation_zones.id", ondelete="SET NULL"),
        nullable=True
    )

    zone = relationship("CultivationZone", backref="devices")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
