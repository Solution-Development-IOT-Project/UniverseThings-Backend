from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from app.db.session import Base


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)

    # Tipo de reporte:
    # Ej: sensor_summary, water_usage, ndvi_analysis, alert_history
    report_type = Column(String(100), nullable=False)

    # Ruta del archivo generado (PDF, CSV, etc.)
    file_path = Column(String(255), nullable=True)

    # Estado del reporte: generated, failed, pending
    status = Column(String(50), nullable=False, default="generated")


    farm_id = Column(
        Integer,
        ForeignKey("farms.id", ondelete="SET NULL"),
        nullable=True
    )
    parcel_id = Column(
        Integer,
        ForeignKey("parcels.id", ondelete="SET NULL"),
        nullable=True
    )
    zone_id = Column(
        Integer,
        ForeignKey("cultivation_zones.id", ondelete="SET NULL"),
        nullable=True
    )

    farm = relationship("Farm", backref="reports")
    parcel = relationship("Parcel", backref="reports")
    zone = relationship("CultivationZone", backref="reports")

    created_by_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True
    )

    created_by = relationship("User", backref="reports")


    generated_at = Column(DateTime(timezone=True), server_default=func.now())

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )
