from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent # путь

class Settings(BaseSettings):
    app_name: str = "Recipe Finder"
    debug: bool = False
    default_page_size: int | None = 10
    max_recipes: int = 1000
    database_url: str

    # Добавляем этот блок для автоматической загрузки из .env
    model_config = SettingsConfigDict(
        env_file= BASE_DIR / ".env",
        extra="ignore" # игнорировать лишние переменные в .env
    )



class SettingsSeed(BaseSettings):
    app_name: str = "Recipe Finder"
    debug: bool = False
    default_page_size: int | None = 10
    max_recipes: int = 1000
    database_url: str

    # Добавляем этот блок для автоматической загрузки из .env
    model_config = SettingsConfigDict(
        env_file= ".env",
        extra="ignore" # игнорировать лишние переменные в .env
    )

settings = Settings()
settings_seed = SettingsSeed()