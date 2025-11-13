from sqlalchemy import Column, Integer, String, Text, DateTime, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Cooperative(Base):
    __tablename__ = "cooperatives"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    contact_name = Column(String(150), nullable=True)
    contact_email = Column(String(150), nullable=True)
    contact_phone = Column(String(50), nullable=True)

    address = Column(String(255), nullable=True)

    # Si luego quieres vincular farms a cooperatives,
    # puedes agregar cooperative_id en Farm y la relación aquí:
    # farms = relationship("Farm", backref="cooperative")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
