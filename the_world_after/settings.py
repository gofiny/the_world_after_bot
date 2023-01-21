from pydantic import BaseSettings


class Settings(BaseSettings):
    IS_WEBHOOK: bool = False
    TELEGRAM_TOKEN: str

    LOG_CONFIG: str


settings = Settings()
