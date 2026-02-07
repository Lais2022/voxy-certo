from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.db.database import SessionLocal

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="API key inválida")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/metrics", dependencies=[Depends(verify_api_key)])
def dashboard_metrics(db: Session = Depends(get_db)) -> dict:
    leads = db.query(func.count(models.Lead.id)).scalar() or 0
    deals = db.query(func.count(models.Deal.id)).scalar() or 0
    activities = db.query(func.count(models.Activity.id)).scalar() or 0
    total_value = db.query(func.coalesce(func.sum(models.Deal.value), 0)).scalar() or 0
    return {
        "leads": leads,
        "deals": deals,
        "activities": activities,
        "total_value": total_value,
    }
