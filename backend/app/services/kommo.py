import hashlib
import hmac

from fastapi import HTTPException

from app.core.config import settings


def validate_signature(payload: dict, signature: str | None) -> None:
    if not settings.kommo_webhook_secret:
        return
    if not signature:
        raise HTTPException(status_code=401, detail="Assinatura ausente")
    digest = hmac.new(
        settings.kommo_webhook_secret.encode("utf-8"),
        msg=str(payload).encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(digest, signature):
        raise HTTPException(status_code=401, detail="Assinatura inválida")
