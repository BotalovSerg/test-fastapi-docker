import os
from pathlib import Path
from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent.parent
SESSIONS_DIR = BASE_DIR / "tg_session"


def get_session_path(phone: str) -> Path:
    session_name = f"session_{phone}"
    return SESSIONS_DIR / session_name


class TelegramBot(BaseModel):
    token: str


class DatebaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = True


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        env_nested_delimiter="_",
        env_prefix="APP_",
    )
    api_v1_prefix: str = "/api/v1"
    bot: TelegramBot
    db: DatebaseConfig


settings = Settings()
