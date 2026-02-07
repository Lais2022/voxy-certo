from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.api.crm_routes import router as crm_router
from app.api.dashboard_routes import router as dashboard_router
from app.api.agent_routes import router as agent_router
from app.core.config import settings
from sqlalchemy import select

from app.db import Base, SessionLocal, engine
from app.db.models import AgentState, PipelineStage

app = FastAPI(title=settings.app_name, version=settings.app_version)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"] ,
    allow_headers=["*"],
)

app.include_router(router)
app.include_router(crm_router)
app.include_router(dashboard_router)
app.include_router(agent_router)


@app.on_event("startup")
def on_startup() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        exists = db.execute(select(PipelineStage).limit(1)).scalar_one_or_none()
        if not exists:
            db.add(PipelineStage(name=settings.crm_default_stage, order_index=0))
            db.commit()
        agent_state = db.execute(select(AgentState).limit(1)).scalar_one_or_none()
        if not agent_state:
            db.add(AgentState(status=settings.agent_default_status, last_reason="Inicialização"))
            db.commit()
