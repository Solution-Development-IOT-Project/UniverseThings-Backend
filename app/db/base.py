# app/db/base.py

# 1) Importa Base desde session.py
from app.db.session import Base

# 2) Importa TODOS los modelos para que se registren en el metadata de Base
from app.models.user import User
from app.models.role import Role
from app.models.user_parcel_access import UserParcelAccess

from app.models.farm import Farm
from app.models.parcel import Parcel
from app.models.cultivation_zone import CultivationZone

from app.models.sensor import Sensor
from app.models.actuator import Actuator
from app.models.device import Device

from app.models.measurement import Measurement
from app.models.alert import Alert

from app.models.camera import Camera
from app.models.image import Image

from app.models.automation_rule import AutomationRule
from app.models.automation_log import AutomationLog
from app.models.rule_actuator_map import RuleActuatorMap

from app.models.threshold_config import ThresholdConfig
from app.models.cooperative import Cooperative
