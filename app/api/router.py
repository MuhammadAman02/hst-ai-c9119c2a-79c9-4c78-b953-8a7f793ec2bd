"""Main API router"""
from fastapi import APIRouter
from app.api.game import router as game_router
from app.api.health import router as health_router

api_router = APIRouter()

# Include sub-routers
api_router.include_router(health_router, tags=["health"])
api_router.include_router(game_router, prefix="/game", tags=["game"])