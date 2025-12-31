from fastapi import FastAPI
from routers.products import router as products_router

app = FastAPI(
    title="Product API",
    description="FastAPI application for managing products",
    version="1.0.0"
)

app.include_router(products_router)

@app.get("/", tags=["root"])
async def root() -> dict:
    return {
        "message": "Welcome to Product API",
        "docs": "/docs"
    }


