import logging

logger = logging.getLogger(__name__)


def process_webhook(source: str, payload: dict) -> None:
    logger.info("Processando webhook", extra={"source": source, "payload": payload})
