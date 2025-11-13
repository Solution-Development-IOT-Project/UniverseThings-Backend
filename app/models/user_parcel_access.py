from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class UserParcelAccess(Base):
    __tablename__ = "user_parcel_access"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    parcel_id = Column(Integer, ForeignKey("parcels.id", ondelete="CASCADE"), nullable=False)

    # Nivel de acceso del usuario a la parcela
    # Ej: "read", "write", "admin"
    access_type = Column(String(20), nullable=False, default="read")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    user = relationship("User", back_populates="parcels")
    parcel = relationship("Parcel", back_populates="users")
