"""Application configuration using pydantic-settings V2"""
from pydantic_settings import BaseSettings
from pydantic import Field, ConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Application settings with environment variable support."""
    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    APP_NAME: str = Field(default="Subway Surfers Game")
    APP_DESCRIPTION: str = Field(default="An endless runner game inspired by Subway Surfers")
    APP_VERSION: str = Field(default="1.0.0")
    DEBUG: bool = Field(default=False)
    
    # Server
    HOST: str = Field(default="0.0.0.0")
    PORT: int = Field(default=8080)
    
    # Security
    SECRET_KEY: str = Field(default="subway-surfers-secret-key-change-in-production")
    
    # Database
    DATABASE_URL: str = Field(default="sqlite:///./data/game.db")
    
    # Game Settings
    GAME_SPEED: float = Field(default=5.0)
    OBSTACLE_SPAWN_RATE: float = Field(default=0.02)
    COIN_SPAWN_RATE: float = Field(default=0.01)
    POWERUP_SPAWN_RATE: float = Field(default=0.005)
    
    # API
    API_PREFIX: str = Field(default="/api")

settings = Settings()