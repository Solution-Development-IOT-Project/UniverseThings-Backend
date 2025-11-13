from fastapi import APIRouter

from app.api.v1.auth import router as auth_router
from app.api.v1.users import router as users_router
from app.api.v1.farms import router as farms_router
from app.api.v1.parcels import router as parcels_router
from app.api.v1.cultivation_zones import router as zones_router
from app.api.v1.sensors import router as sensors_router
from app.api.v1.actuators import router as actuators_router
from app.api.v1.devices import router as devices_router
from app.api.v1.measurements import router as measurements_router
from app.api.v1.alerts import router as alerts_router
from app.api.v1.cameras import router as cameras_router
from app.api.v1.images import router as images_router
from app.api.v1.automation import router as automation_router
from app.api.v1.threshold_config import router as threshold_router
from app.api.v1.cooperatives import router as cooperatives_router
from app.api.v1.reports import router as reports_router
from app.api.v1.notifications import router as notifications_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(farms_router)
api_router.include_router(parcels_router)
api_router.include_router(zones_router)
api_router.include_router(sensors_router)
api_router.include_router(actuators_router)
api_router.include_router(devices_router)
api_router.include_router(measurements_router)
api_router.include_router(alerts_router)
api_router.include_router(cameras_router)
api_router.include_router(images_router)
api_router.include_router(automation_router)
api_router.include_router(threshold_router)
api_router.include_router(cooperatives_router)
api_router.include_router(reports_router)
api_router.include_router(notifications_router)
