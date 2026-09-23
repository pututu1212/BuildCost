from fastapi import APIRouter

from backend.app.api import materials, prices, projects

api_router = APIRouter(prefix="/v1")

api_router.include_router(materials.router)
api_router.include_router(prices.router)
api_router.include_router(projects.router)