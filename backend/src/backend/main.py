from fastapi import FastAPI
from src.backend.api.v1.recipes import router as recipes_router

# Создали объект приложения FASTapi
app = FastAPI(
    title="Recipe Finder API",  # отображается в swagger ui название
    description="Платформа для Рецептов",  # описание проекта можно использовать марк даун
    version="0.1.0"
)


@app.get("/")
async def root():
    return {"message": "Recipe Finder API is running"}


@app.get("/health")
async def health_check():
    return {"status": "ok", "version": "0.1.0"}

app.include_router(recipes_router,prefix="/api/v1")