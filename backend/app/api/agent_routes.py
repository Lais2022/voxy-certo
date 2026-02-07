from datetime import datetime

from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models, schemas
from app.db.database import SessionLocal

router = APIRouter(prefix="/agent", tags=["agent"])


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="API key inválida")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_state(db: Session) -> models.AgentState:
    state = db.query(models.AgentState).first()
    if not state:
        state = models.AgentState(status="paused", last_reason="Inicialização")
        db.add(state)
        db.commit()
        db.refresh(state)
    return state


@router.get("/state", response_model=schemas.AgentStateRead, dependencies=[Depends(verify_api_key)])
def read_state(db: Session = Depends(get_db)):
    return get_state(db)


@router.put("/state", response_model=schemas.AgentStateRead, dependencies=[Depends(verify_api_key)])
def update_state(payload: schemas.AgentStateUpdate, db: Session = Depends(get_db)):
    state = get_state(db)
    state.status = payload.status
    state.last_reason = payload.last_reason
    state.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(state)
    return state


@router.post("/scripts", response_model=schemas.AgentScriptRead, dependencies=[Depends(verify_api_key)])
def create_script(payload: schemas.AgentScriptCreate, db: Session = Depends(get_db)):
    script = models.AgentScript(**payload.dict())
    db.add(script)
    db.commit()
    db.refresh(script)
    return script


@router.get("/scripts", response_model=list[schemas.AgentScriptRead], dependencies=[Depends(verify_api_key)])
def list_scripts(db: Session = Depends(get_db)):
    return db.query(models.AgentScript).order_by(models.AgentScript.created_at.desc()).all()
