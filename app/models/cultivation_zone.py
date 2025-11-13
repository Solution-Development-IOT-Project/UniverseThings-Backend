from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class CultivationZone(Base):
    __tablename__ = "cultivation_zones"


    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    crop_type = Column(String(150), nullable=True)       # tipo de cultivo (maíz, papa…)
    description = Column(Text, nullable=True)
    area_m2 = Column(Float, nullable=True)               # tamaño en m² de la zona

    parcel_id = Column(Integer, ForeignKey("parcels.id", ondelete="CASCADE"), nullable=False)

    parcel = relationship("Parcel", back_populates="zones")



    sensors = relationship(
        "Sensor",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    actuators = relationship(
        "Actuator",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    cameras = relationship(
        "Camera",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    automation_rules = relationship(
        "AutomationRule",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    threshold_configs = relationship(
        "ThresholdConfig",
        back_populates="zone",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
