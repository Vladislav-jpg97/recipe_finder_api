from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

class Settings(BaseSettings):
    app_name: str = "Recipe Finder"
    debug: bool = False
    default_page_size: int | None = 10
    max_recipes: int = 1000
    database_url: str
    secret_key: str
    algorithm : str
    access_token_expire_minutes: int
    refresh_token_expire_days: int
    redis_url: str

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.docker"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()