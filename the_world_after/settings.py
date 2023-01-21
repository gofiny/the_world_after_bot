from pydantic import BaseSettings, PostgresDsn


class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    APP_URL: str
    APP_EVENTS_PATH: str = "/events"

    IS_WEBHOOK: bool = False
    TELEGRAM_TOKEN: str

    LOG_CONFIG: str

    DB_DSN: PostgresDsn


settings = Settings()
