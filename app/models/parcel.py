from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Parcel(Base):
    __tablename__ = "parcels"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(150), nullable=False)
    description = Column(Text, nullable=True)
    area_hectares = Column(Float, nullable=True)


    farm_id = Column(Integer, ForeignKey("farms.id", ondelete="CASCADE"), nullable=False)

    farm = relationship("Farm", back_populates="parcels")


    zones = relationship(
        "CultivationZone",
        back_populates="parcel",
        cascade="all, delete-orphan"
    )

    users = relationship(
        "UserParcelAccess",
        back_populates="parcel",
        cascade="all, delete-orphan"
    )

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
