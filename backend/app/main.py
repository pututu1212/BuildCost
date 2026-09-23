from fastapi import FastAPI
from sqlalchemy import text

from backend.app.api.router import api_router
from backend.app.db.session import engine

app = FastAPI(
    title="BUILDcost API",
    description="India-first construction cost intelligence platform",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "name": "BUILDcost API",
        "status": "online",
        "version": "0.1.0",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
    }


@app.get("/health/database")
def database_health():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

    return {
        "database": "connected",
        "result": result.scalar(),
    }