from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.sensor import Sensor
from app.models.threshold_config import ThresholdConfig
from app.models.measurement import Measurement


class AlertService:
    """
    Servicio centralizado para generar alertas basadas en:
    - mediciones
    - umbrales
    - severidad crítica / warning
    """

    def __init__(self, db: Session):
        self.db = db

    # ========================================================
    # MÉTODO PRINCIPAL → LLAMADO DESDE measurement_service
    # ========================================================
    def evaluate_measurement(self, measurement: Measurement) -> Optional[Alert]:
        """
        Evalúa una medición recién creada y genera una alerta si corresponde.
        """

        sensor = (
            self.db.query(Sensor)
            .filter(Sensor.id == measurement.sensor_id)
            .first()
        )
        if not sensor:
            return None

        # Obtener umbrales configurados
        thresholds: List[ThresholdConfig] = (
            self.db.query(ThresholdConfig)
            .filter(ThresholdConfig.sensor_id == sensor.id)
            .filter(ThresholdConfig.is_active == True)
            .all()
        )

        if not thresholds:
            return None

        for t in thresholds:
            alert = self._check_threshold(t, measurement, sensor.zone_id)
            if alert:
                return alert

        return None

    # ========================================================
    # EVALUAR UMBRAL
    # ========================================================
    def _check_threshold(
        self,
        threshold: ThresholdConfig,
        measurement: Measurement,
        zone_id: int,
    ) -> Optional[Alert]:
        """
        Evalúa una medición según un threshold específico.
        """

        value = measurement.value
        param = threshold.parameter

        # ===============================
        # 1. Evaluaciones críticas
        # ===============================
        critical = False
        warn = False

        # Operador principal
        op = threshold.operator

        if op == "between":
            if threshold.min_value is not None and value < threshold.min_value:
                critical = True
            if threshold.max_value is not None and value > threshold.max_value:
                critical = True
        elif op == ">":
            if value > threshold.max_value:
                critical = True
        elif op == "<":
            if value < threshold.min_value:
                critical = True
        elif op == ">=":
            if threshold.max_value is not None and value >= threshold.max_value:
                critical = True
        elif op == "<=":
            if threshold.min_value is not None and value <= threshold.min_value:
                critical = True

        # ===============================
        # 2. Evaluaciones warning
        # ===============================
        if not critical:
            if threshold.warn_min is not None and value < threshold.warn_min:
                warn = True
            if threshold.warn_max is not None and value > threshold.warn_max:
                warn = True

        # ===============================
        # 3. ¿Generamos alerta?
        # ===============================
        if not critical and not warn:
            return None

        severity = "critical" if critical else "warning"

        message = f"Valor anómalo en {param}: {value}"
        details = (
            f"Medición fuera de rango. Min: {threshold.min_value}, "
            f"Max: {threshold.max_value}, WarnMin: {threshold.warn_min}, WarnMax: {threshold.warn_max}"
        )

        # ===============================
        # 4. Crear alerta
        # ===============================
        alert = Alert(
            message=message,
            details=details,
            severity=severity,
            sensor_id=measurement.sensor_id,
            zone_id=zone_id,
            created_at=datetime.utcnow(),
        )

        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)

        return alert

    # ========================================================
    # METODO ADICIONAL: FORZAR ALERTA
    # ========================================================
    def create_manual_alert(
        self,
        zone_id: int,
        message: str,
        severity: str = "info",
        details: Optional[str] = None,
        sensor_id: Optional[int] = None,
    ) -> Alert:
        """Crear una alerta manual desde la API."""
        alert = Alert(
            message=message,
            severity=severity,
            details=details,
            zone_id=zone_id,
            sensor_id=sensor_id,
            created_at=datetime.utcnow(),
        )
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert
