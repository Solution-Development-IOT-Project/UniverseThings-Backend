import json
from datetime import datetime
from typing import Optional, List

from sqlalchemy.orm import Session

from app.models.automation_rule import AutomationRule
from app.models.automation_log import AutomationLog
from app.models.rule_actuator_map import RuleActuatorMap
from app.models.actuator import Actuator
from app.models.sensor import Sensor
from app.models.measurement import Measurement


class AutomationService:
    """
    Servicio para evaluar reglas de automatización y aplicar acciones
    sobre actuadores (encender/apagar, etc.).
    """

    def __init__(self, db: Session):
        self.db = db

    # ========================================================
    # ENTRYPOINT PRINCIPAL → LLAMADO DESDE INGESTA DE MEDICIONES
    # ========================================================
    def handle_new_measurement(self, measurement: Measurement) -> None:
        """
        Se llama cuando se registra una nueva medición.
        - Busca reglas activas asociadas a la zona del sensor.
        - Evalúa cada regla con esta medición.
        - Ejecuta acciones si corresponde.
        """

        sensor: Optional[Sensor] = (
            self.db.query(Sensor)
            .filter(Sensor.id == measurement.sensor_id)
            .first()
        )
        if not sensor or not sensor.zone_id:
            return

        zone_id = sensor.zone_id

        rules: List[AutomationRule] = (
            self.db.query(AutomationRule)
            .filter(AutomationRule.zone_id == zone_id)
            .filter(AutomationRule.is_active == True)
            .order_by(AutomationRule.priority.asc())
            .all()
        )

        for rule in rules:
            self._evaluate_and_execute(rule, measurement)

    # ========================================================
    # EVALUAR UNA REGLA Y EJECUTAR ACCIONES
    # ========================================================
    def _evaluate_and_execute(
        self,
        rule: AutomationRule,
        measurement: Optional[Measurement] = None,
    ) -> None:
        """
        Evalúa una regla dada, opcionalmente con una medición reciente.
        Si la condición es verdadera, ejecuta acciones sobre actuadores
        vinculados a la regla y registra logs.
        """

        try:
            condition_data = json.loads(rule.condition)
        except Exception:
            # Si el JSON está mal formado, registramos un log de fallo
            self._create_log(
                rule=rule,
                status="failed",
                message="Error al parsear condición",
                details=f"condition={rule.condition}",
                sensor_id=measurement.sensor_id if measurement else None,
                zone_id=rule.zone_id,
                action_executed=False,
            )
            return

        should_trigger = self._evaluate_condition(condition_data, measurement)

        if not should_trigger:
            # Log opcional de "skipped"
            self._create_log(
                rule=rule,
                status="skipped",
                message="Condición no cumplida",
                details=f"condition={rule.condition}",
                sensor_id=measurement.sensor_id if measurement else None,
                zone_id=rule.zone_id,
                action_executed=False,
            )
            return

        # Si se cumple la condición → ejecutar acciones sobre actuadores
        rule_links: List[RuleActuatorMap] = rule.actuators or []

        if not rule_links:
            # No hay actuadores asociados, pero la regla se disparó
            self._create_log(
                rule=rule,
                status="triggered",
                message="Regla disparada sin actuadores asociados",
                details=f"condition={rule.condition}",
                sensor_id=measurement.sensor_id if measurement else None,
                zone_id=rule.zone_id,
                action_executed=False,
            )
            return

        # Ejecutamos acción por cada actuador
        for link in rule_links:
            actuator: Optional[Actuator] = link.actuator
            if not actuator:
                self._create_log(
                    rule=rule,
                    status="failed",
                    message="Actuador asociado no encontrado",
                    details=f"rule_actuator_map_id={link.id}",
                    sensor_id=measurement.sensor_id if measurement else None,
                    zone_id=rule.zone_id,
                    action_executed=False,
                )
                continue

            # Aplicar acción: encender/apagar
            try:
                actuator.is_on = bool(link.desired_state)
                # Podrías usar duration_seconds con otro proceso (job async)
                self.db.add(actuator)
                self.db.commit()
                self.db.refresh(actuator)

                self._create_log(
                    rule=rule,
                    status="triggered",
                    message=f"Acción aplicada a actuador {actuator.id}",
                    details=(
                        f"desired_state={link.desired_state}, "
                        f"duration_seconds={link.duration_seconds}"
                    ),
                    sensor_id=measurement.sensor_id if measurement else None,
                    zone_id=rule.zone_id,
                    actuator_id=actuator.id,
                    action_executed=True,
                )
            except Exception as e:
                self.db.rollback()
                self._create_log(
                    rule=rule,
                    status="failed",
                    message=f"Error aplicando acción en actuador {actuator.id}",
                    details=str(e),
                    sensor_id=measurement.sensor_id if measurement else None,
                    zone_id=rule.zone_id,
                    actuator_id=actuator.id,
                    action_executed=False,
                )

    # ========================================================
    # EVALUACIÓN DE CONDICIÓN (SIMPLE, PERO EXTENDIBLE)
    # ========================================================
    def _evaluate_condition(
        self,
        condition: dict,
        measurement: Optional[Measurement],
    ) -> bool:
        """
        Evalúa la condición de una regla.
        Diseño simple, pero fácil de extender.

        Soporta formatos como:
        - {"type": "always", "value": true}
        - {"type": "measurement", "sensor_id": 3, "operator": ">", "value": 30}

        Si necesitas más lógica (AND/OR múltiples condiciones),
        puedes extender este método.
        """

        ctype = condition.get("type", "measurement")

        # Caso trivial: siempre verdadero
        if ctype == "always":
            return bool(condition.get("value", True))

        # Caso estándar: basado en medición
        if ctype == "measurement":
            if measurement is None:
                return False

            # Si se especifica sensor_id, validar que corresponda
            expected_sensor_id = condition.get("sensor_id")
            if expected_sensor_id is not None and measurement.sensor_id != expected_sensor_id:
                return False

            operator = condition.get("operator", ">")
            target_value = condition.get("value")
            min_value = condition.get("min")
            max_value = condition.get("max")

            current_value = measurement.value

            # Operadores soportados
            if operator == ">":
                return target_value is not None and current_value > target_value
            elif operator == "<":
                return target_value is not None and current_value < target_value
            elif operator == ">=":
                return target_value is not None and current_value >= target_value
            elif operator == "<=":
                return target_value is not None and current_value <= target_value
            elif operator == "==":
                return target_value is not None and current_value == target_value
            elif operator == "between":
                if min_value is None or max_value is None:
                    return False
                return min_value <= current_value <= max_value

        # Si no se reconoce el tipo/formato → no se dispara
        return False

    # ========================================================
    # CREACIÓN DE LOGS
    # ========================================================
    def _create_log(
        self,
        rule: AutomationRule,
        status: str,
        message: str,
        details: Optional[str] = None,
        sensor_id: Optional[int] = None,
        zone_id: Optional[int] = None,
        actuator_id: Optional[int] = None,
        action_executed: bool = False,
    ) -> AutomationLog:
        log = AutomationLog(
            rule_id=rule.id,
            status=status,
            message=message,
            details=details,
            action_executed=action_executed,
            actuator_id=actuator_id,
            sensor_id=sensor_id,
            zone_id=zone_id or rule.zone_id,
            executed_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
        )
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
