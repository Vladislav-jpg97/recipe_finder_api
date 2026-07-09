from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Recipe Finder"
    debug: bool = False
    default_page_size: int | None = 10
    max_recipes: int = 1000


settings = Settings()