from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import SessionLocal, engine
from app.db.init_db import init_db
from app.db import base as models_base

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version="1.0.0",
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        description="Backend IoT AgroDrone con FastAPI + MySQL"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # cambiar a dominios específicos en producción
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    models_base.Base.metadata.create_all(bind=engine)

    @app.on_event("startup")
    def startup_event():
        db = SessionLocal()
        init_db(db)  # carga roles + admin si no existen
        db.close()

    @app.get("/")
    def root():
        return {
            "message": "AgroDrone Backend funcionando correctamente",
            "api_docs": f"{settings.API_V1_STR}/docs"
        }

    return app


app = create_app()
