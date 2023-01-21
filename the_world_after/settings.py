from typing import Optional

from pydantic import BaseSettings, PositiveInt, PostgresDsn


class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_URL: str
    APP_EVENTS_PATH: str = "/events"

    IS_WEBHOOK: bool = False
    TELEGRAM_TOKEN: str
    TELEGRAM_MAX_CONNECTIONS: PositiveInt = 50
    TELEGRAM_SECRET_KEY: Optional[str] = None

    LOG_CONFIG: str

    DB_DSN: PostgresDsn


settings = Settings()
