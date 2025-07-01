"""FastAPI router setup"""
from fastapi import FastAPI
from app.api import api_router

def setup_routers(app: FastAPI, api_prefix: str = "/api"):
    """Setup application routers"""
    app.include_router(api_router, prefix=api_prefix)