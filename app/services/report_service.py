from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.report import Report
from app.models.user import User


class ReportService:


    def __init__(self, db: Session):
        self.db = db

    def create_report_entry(
        self,
        title: str,
        report_type: str,
        created_by: User,
        description: Optional[str] = None,
        farm_id: Optional[int] = None,
        parcel_id: Optional[int] = None,
        zone_id: Optional[int] = None,
        status: str = "pending",
    ) -> Report:

        now = datetime.utcnow()

        report = Report(
            title=title,
            description=description,
            report_type=report_type,
            file_path=None,
            status=status,
            farm_id=farm_id,
            parcel_id=parcel_id,
            zone_id=zone_id,
            created_by_id=created_by.id,
            generated_at=None if status == "pending" else now,
            created_at=now,
        )

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def mark_report_generated(
        self,
        report: Report,
        file_path: str,
    ) -> Report:
        report.status = "generated"
        report.file_path = file_path
        report.generated_at = datetime.utcnow()
        report.updated_at = datetime.utcnow()

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def mark_report_failed(
        self,
        report: Report,
        error_message: Optional[str] = None,
    ) -> Report:

        report.status = "failed"
        if error_message:
            # concatenamos el error al description
            if report.description:
                report.description += f"\n[ERROR] {error_message}"
            else:
                report.description = f"[ERROR] {error_message}"

        report.updated_at = datetime.utcnow()

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def reset_to_pending(self, report: Report) -> Report:


        report.status = "pending"
        report.file_path = None
        report.generated_at = None
        report.updated_at = datetime.utcnow()

        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def list_reports_by_user(
        self,
        user_id: int,
        limit: int = 50,
    ) -> List[Report]:

        q = (
            self.db.query(Report)
            .filter(Report.created_by_id == user_id)
            .order_by(Report.created_at.desc())
            .limit(limit)
        )
        return q.all()

    def list_reports_by_zone(
        self,
        zone_id: int,
        limit: int = 50,
    ) -> List[Report]:

        q = (
            self.db.query(Report)
            .filter(Report.zone_id == zone_id)
            .order_by(Report.created_at.desc())
            .limit(limit)
        )
        return q.all()

    def list_reports_by_farm(
        self,
        farm_id: int,
        limit: int = 50,
    ) -> List[Report]:

        q = (
            self.db.query(Report)
            .filter(Report.farm_id == farm_id)
            .order_by(Report.created_at.desc())
            .limit(limit)
        )
        return q.all()

    def list_reports_by_type(
        self,
        report_type: str,
        limit: int = 50,
    ) -> List[Report]:

        q = (
            self.db.query(Report)
            .filter(Report.report_type == report_type)
            .order_by(Report.created_at.desc())
            .limit(limit)
        )
        return q.all()
