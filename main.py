"""Subway Surfers-like Game - Production Entry Point"""
import os
import sys
from dotenv import load_dotenv
from nicegui import ui

# Load environment variables
load_dotenv()

# Import the game application
try:
    import app.main  # noqa: F401
except ImportError as e:
    print(f"Error importing app.main: {e}")
    sys.exit(1)

# Create FastAPI app for API endpoints
from fastapi import FastAPI
from app.core import settings, app_logger, setup_middleware, setup_routers, setup_error_handlers

app = FastAPI(
    title="Subway Surfers Game",
    description="An endless runner game inspired by Subway Surfers",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# Setup FastAPI components
setup_error_handlers(app)
setup_middleware(app)
setup_routers(app, api_prefix="/api")

# Setup database
try:
    from app.core.database import create_tables
    create_tables()
    app_logger.info("Database tables created successfully")
except Exception as e:
    app_logger.error(f"Database setup error: {e}")

if __name__ in {"__main__", "__mp_main__"}:
    try:
        # Setup NiceGUI integration
        from app.core.nicegui_setup import setup_nicegui
        setup_nicegui(app)
        
        app_logger.info(f"Starting Subway Surfers Game at {settings.HOST}:{settings.PORT}")
        ui.run(
            host=settings.HOST,
            port=settings.PORT,
            title="Subway Surfers Game",
            uvicorn_logging_level='info' if settings.DEBUG else 'warning',
            reload=settings.DEBUG,
            storage_secret=settings.SECRET_KEY,
            favicon="🚇"
        )
    except Exception as e:
        import traceback
        app_logger.critical(f"Error starting game: {e}")
        app_logger.critical(traceback.format_exc())
        sys.exit(1)