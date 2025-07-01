"""Main game application with NiceGUI interface"""
from nicegui import ui
from app.frontend.game_ui import GameUI
from app.core.logging import app_logger

# Initialize the game UI
game_ui = GameUI()

@ui.page('/')
async def index():
    """Main game page"""
    try:
        await game_ui.create_game_page()
        app_logger.info("Game page loaded successfully")
    except Exception as e:
        app_logger.error(f"Error loading game page: {e}")
        ui.label("Error loading game. Please refresh the page.").classes('text-red-500 text-center')

@ui.page('/leaderboard')
async def leaderboard():
    """Leaderboard page"""
    try:
        await game_ui.create_leaderboard_page()
        app_logger.info("Leaderboard page loaded successfully")
    except Exception as e:
        app_logger.error(f"Error loading leaderboard: {e}")
        ui.label("Error loading leaderboard. Please refresh the page.").classes('text-red-500 text-center')