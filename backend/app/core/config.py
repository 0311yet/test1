from pydantic_settings import BaseSettings
from functools import lru_cache
import os

class Settings(BaseSettings):
    """Application settings"""
    
    APP_NAME: str = "Crypto Trading System"
    APP_VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: str = "postgresql://trader:traderpassword@postgres:5432/crypto_trading"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379/0"
    
    # OKX
    OKX_API_KEY: str = os.getenv("OKX_API_KEY", "")
    OKX_SECRET_KEY: str = os.getenv("OKX_SECRET_KEY", "")
    OKX_PASSPHRASE: str = os.getenv("OKX_PASSPHRASE", "")
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # WebSocket
    WS_HEARTBEAT_INTERVAL: int = 30
    
    # Cache
    CACHE_TTL: int = 300
    
    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
