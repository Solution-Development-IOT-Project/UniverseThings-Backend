from datetime import datetime
from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User
from app.models.alert import Alert
from app.models.automation_rule import AutomationRule
from app.models.report import Report


class NotificationService:
    """
    Servicio centralizado para crear y gestionar notificaciones.
    """

    def __init__(self, db: Session):
        self.db = db

    def notify_user(
        self,
        user_id: int,
        title: str,
        message: str,
        notification_type: str = "system",
        channel: Optional[str] = None,
        alert_id: Optional[int] = None,
        sensor_id: Optional[int] = None,
        actuator_id: Optional[int] = None,
        zone_id: Optional[int] = None,
    ) -> Notification:


        notif = Notification(
            title=title,
            message=message,
            notification_type=notification_type,
            channel=channel,
            user_id=user_id,
            alert_id=alert_id,
            sensor_id=sensor_id,
            actuator_id=actuator_id,
            zone_id=zone_id,
            created_at=datetime.utcnow(),
            is_read=False,
        )

        self.db.add(notif)
        self.db.commit()
        self.db.refresh(notif)
        return notif

    def notify_users(
        self,
        user_ids: Iterable[int],
        title: str,
        message: str,
        notification_type: str = "system",
        channel: Optional[str] = None,
        alert_id: Optional[int] = None,
        sensor_id: Optional[int] = None,
        actuator_id: Optional[int] = None,
        zone_id: Optional[int] = None,
    ) -> List[Notification]:


        notifications: List[Notification] = []

        now = datetime.utcnow()
        for uid in user_ids:
            notif = Notification(
                title=title,
                message=message,
                notification_type=notification_type,
                channel=channel,
                user_id=uid,
                alert_id=alert_id,
                sensor_id=sensor_id,
                actuator_id=actuator_id,
                zone_id=zone_id,
                created_at=now,
                is_read=False,
            )
            self.db.add(notif)
            notifications.append(notif)

        self.db.commit()
        for n in notifications:
            self.db.refresh(n)

        return notifications


    def notify_users_from_alert(
        self,
        alert: Alert,
        target_users: Iterable[User],
        channel: Optional[str] = "internal",
    ) -> List[Notification]:


        title = f"Alerta ({alert.severity}) en zona {alert.zone_id}"
        message = alert.message

        user_ids = [u.id for u in target_users]
        return self.notify_users(
            user_ids=user_ids,
            title=title,
            message=message,
            notification_type="alert",
            channel=channel,
            alert_id=alert.id,
            sensor_id=alert.sensor_id,
            zone_id=alert.zone_id,
        )

    def notify_from_automation_rule(
        self,
        rule: AutomationRule,
        target_users: Iterable[User],
        message: Optional[str] = None,
        channel: Optional[str] = "internal",
    ) -> List[Notification]:


        title = f"Regla ejecutada: {rule.name}"
        msg = message or f"La regla '{rule.name}' ha sido ejecutada o requiere atención."

        user_ids = [u.id for u in target_users]
        return self.notify_users(
            user_ids=user_ids,
            title=title,
            message=msg,
            notification_type="automation",
            channel=channel,
            zone_id=rule.zone_id,
        )

    def notify_report_generated(
        self,
        report: Report,
        target_users: Iterable[User],
        channel: Optional[str] = "internal",
    ) -> List[Notification]:

        status = report.status
        title = f"Reporte {status}: {report.title}"

        if status == "generated":
            msg = f"El reporte '{report.title}' ha sido generado correctamente."
        elif status == "failed":
            msg = f"El reporte '{report.title}' ha fallado. Revise el sistema."
        else:
            msg = f"Estado del reporte '{report.title}': {status}."

        user_ids = [u.id for u in target_users]
        return self.notify_users(
            user_ids=user_ids,
            title=title,
            message=msg,
            notification_type="report",
            channel=channel,
            zone_id=report.zone_id,
        )

    def mark_all_read_for_user(self, user_id: int) -> int:

        q = (
            self.db.query(Notification)
            .filter(Notification.user_id == user_id)
            .filter(Notification.is_read == False)
        )

        count = 0
        now = datetime.utcnow()
        for notif in q.all():
            notif.is_read = True
            notif.read_at = now
            self.db.add(notif)
            count += 1

        if count > 0:
            self.db.commit()

        return count
