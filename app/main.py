from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.db.init_db import init_db
from app.db import base as models_base

from app.api import api_router

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",     # opcional: mover docs a /api/v1/docs
        redoc_url=f"{settings.API_V1_STR}/redoc",   # opcional
        description="Backend IoT AgroDrone con FastAPI + MySQL",
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # en prod restringir
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Crear tablas
    models_base.Base.metadata.create_all(bind=engine)

    # Datos iniciales
    @app.on_event("startup")
    def startup_event():
        db = SessionLocal()
        init_db(db)
        db.close()

    # ✅ MONTAR TODOS LOS ENDPOINTS /api/v1/...
    app.include_router(api_router, prefix=settings.API_V1_STR)

    # Root simple
    @app.get("/")
    def root():
        return {
            "message": "AgroDrone Backend funcionando correctamente",
            "api_docs": f"{settings.API_V1_STR}/docs",
        }

    return app


app = create_app()