from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


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
