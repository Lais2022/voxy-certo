from fastapi import APIRouter, Depends, Header, HTTPException, Request
from rq import Queue
from redis import Redis

from app.core.config import settings
from app.services import kommo, lovable, zapsuite
from app.workers.tasks import process_webhook

router = APIRouter()


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if settings.api_key and x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail="API key inválida")


def get_queue() -> Queue:
    redis_conn = Redis.from_url(settings.redis_url)
    return Queue("webhooks", connection=redis_conn)


@router.get("/health")
def healthcheck() -> dict:
    return {"status": "ok", "environment": settings.app_env}


@router.post("/webhooks/lovable")
async def lovable_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
    queue: Queue = Depends(get_queue),
    _=Depends(verify_api_key),
) -> dict:
    payload = await request.json()
    lovable.validate_signature(payload, x_signature)
    queue.enqueue(process_webhook, "lovable", payload)
    return {"status": "queued"}


@router.post("/webhooks/kommo")
async def kommo_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
    queue: Queue = Depends(get_queue),
    _=Depends(verify_api_key),
) -> dict:
    payload = await request.json()
    kommo.validate_signature(payload, x_signature)
    queue.enqueue(process_webhook, "kommo", payload)
    return {"status": "queued"}


@router.post("/webhooks/zapsuite")
async def zapsuite_webhook(
    request: Request,
    x_signature: str | None = Header(default=None),
    queue: Queue = Depends(get_queue),
    _=Depends(verify_api_key),
) -> dict:
    payload = await request.json()
    zapsuite.validate_signature(payload, x_signature)
    queue.enqueue(process_webhook, "zapsuite", payload)
    return {"status": "queued"}
