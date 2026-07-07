from fastapi import FastAPI

app = FastAPI(
    title="Recipe Finder API",
    description="Рецепты блюд",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {"message": "Recipe Finder API is running"}


@app.get("/health")
async def health():
    return {"status": "ok", "version": "0.1.0"}
