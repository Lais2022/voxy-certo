from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models, schemas
from app.db.database import SessionLocal

router = APIRouter(prefix="/crm", tags=["crm"])


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="API key inválida")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/leads", response_model=schemas.LeadRead, dependencies=[Depends(verify_api_key)])
def create_lead(payload: schemas.LeadCreate, db: Session = Depends(get_db)):
    lead = models.Lead(**payload.dict())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("/leads", response_model=list[schemas.LeadRead], dependencies=[Depends(verify_api_key)])
def list_leads(db: Session = Depends(get_db)):
    return db.query(models.Lead).order_by(models.Lead.created_at.desc()).all()


@router.post("/stages", response_model=schemas.PipelineStageRead, dependencies=[Depends(verify_api_key)])
def create_stage(payload: schemas.PipelineStageCreate, db: Session = Depends(get_db)):
    stage = models.PipelineStage(**payload.dict())
    db.add(stage)
    db.commit()
    db.refresh(stage)
    return stage


@router.get("/stages", response_model=list[schemas.PipelineStageRead], dependencies=[Depends(verify_api_key)])
def list_stages(db: Session = Depends(get_db)):
    return db.query(models.PipelineStage).order_by(models.PipelineStage.order_index).all()


@router.post("/deals", response_model=schemas.DealRead, dependencies=[Depends(verify_api_key)])
def create_deal(payload: schemas.DealCreate, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, payload.lead_id)
    stage = db.get(models.PipelineStage, payload.stage_id)
    if not lead or not stage:
        raise HTTPException(status_code=404, detail="Lead ou etapa não encontrada")
    deal = models.Deal(**payload.dict())
    db.add(deal)
    db.commit()
    db.refresh(deal)
    return deal


@router.get("/deals", response_model=list[schemas.DealRead], dependencies=[Depends(verify_api_key)])
def list_deals(db: Session = Depends(get_db)):
    return db.query(models.Deal).order_by(models.Deal.created_at.desc()).all()


@router.post("/activities", response_model=schemas.ActivityRead, dependencies=[Depends(verify_api_key)])
def create_activity(payload: schemas.ActivityCreate, db: Session = Depends(get_db)):
    lead = db.get(models.Lead, payload.lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead não encontrado")
    activity = models.Activity(**payload.dict())
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@router.get("/activities", response_model=list[schemas.ActivityRead], dependencies=[Depends(verify_api_key)])
def list_activities(db: Session = Depends(get_db)):
    return db.query(models.Activity).order_by(models.Activity.created_at.desc()).all()
