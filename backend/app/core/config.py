from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Voxy Backend"
    app_env: str = "production"
    app_version: str = "1.0.0"
    app_log_level: str = "info"
    app_base_url: str = "http://localhost:8000"

    api_key_header: str = "X-Api-Key"
    api_key: str = ""
    allowed_origins: str = "*"

    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "voxy"
    postgres_user: str = "voxy"
    postgres_password: str = ""
    database_url: str = "postgresql+psycopg://voxy:password@postgres:5432/voxy"

    redis_url: str = "redis://redis:6379/0"

    lovable_webhook_secret: str = ""
    whatsapp_provider: str = "kommo"
    kommo_webhook_secret: str = ""
    zapsuite_webhook_secret: str = ""

    sentry_dsn: str = ""

    crm_default_stage: str = "Novo Lead"

    agent_default_status: str = "paused"

    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def allowed_origins_list(self) -> list[str]:
        if self.allowed_origins.strip() == "*":
            return ["*"]
        return [origin.strip() for origin in self.allowed_origins.split(",") if origin.strip()]


settings = Settings()
