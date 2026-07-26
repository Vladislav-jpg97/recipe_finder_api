from fastapi import FastAPI
from backend.api.v1.cuisines import router as cuisines_router
from backend.api.v1.new_recipes import router as new_recipes_router
from backend.api.v1.ingredients import router as ingredients_router
from backend.api.v1.reviews import router as reviews_router
from backend.api.v1.auth import router as auth_router
from backend.core.config import settings
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

app.include_router(cuisines_router,prefix="/api/v1")
app.include_router(new_recipes_router,prefix="/api/v1")
app.include_router(ingredients_router,prefix="/api/v1")
app.include_router(reviews_router,prefix="/api/v1")
app.include_router(auth_router,prefix="/api/v1")