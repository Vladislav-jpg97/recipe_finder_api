from fastapi import FastAPI
from src.backend.api.v1.recipes import router as recipes_router
from src.backend.core.config import settings
# Создали объект приложения FASTapi
app = FastAPI(
    title=f"{settings.app_name}",
    description="Платформа для Рецептов",
    version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": f"{settings.app_name} is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

app.include_router(recipes_router,prefix="/api/v1")