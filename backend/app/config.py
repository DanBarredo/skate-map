"""
Application configuration settings using pydantic-settings.

Loads environment variables from .env file and validates them.
"""

from functools import lru_cache
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    All settings can be overridden via environment variables using
    the uppercase version of the attribute name.
    
    Example:
        DATABASE_URL=postgresql://... python app.py
    """

    # Database Configuration
    database_url: str = "postgresql://user:password@localhost:5432/skate_map"
    """PostgreSQL connection URL"""

    # JWT Configuration (for fastapi-users)
    jwt_secret_key: str = "supersecret"
    """Secret key for JWT token generation. Must be strong in production."""
    
    jwt_algorithm: str = "HS256"
    """JWT algorithm for token signing"""
    
    jwt_expiration_seconds: int = 3600
    """JWT token expiration time in seconds (default: 1 hour)"""

    # Admin Configuration (for starlette-admin)
    admin_username: str = "admin"
    """Default admin username for dashboard access"""
    
    admin_password: str = "admin"
    """Default admin password for dashboard access"""

    # Application Configuration
    debug: bool = False
    """Enable debug mode (hot reload, verbose errors)"""
    
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    """Comma-separated list of allowed CORS origins"""

    class Config:
        """Pydantic settings configuration"""
        env_file = ".env"
        """Load environment variables from .env file"""
        
        env_file_encoding = "utf-8"
        """Encoding for .env file"""
        
        case_sensitive = False
        """Allow lowercase environment variable names"""

    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list of URLs"""
        return [origin.strip() for origin in self.cors_origins.split(",")]


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Uses @lru_cache to ensure only one Settings instance is created
    per application lifetime, reducing file I/O.
    
    Returns:
        Settings: Application settings instance
        
    Example:
        settings = get_settings()
        print(settings.database_url)
    """
    return Settings()