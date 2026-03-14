import redis
from core.config import get_settings

settings = get_settings()

class RedisManager:
    """Redis connection manager"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._redis = None
        return cls._instance
    
    def get_client(self) -> redis.Redis:
        """Get Redis client instance"""
        if self._redis is None:
            self._redis = redis.from_url(
                settings.REDIS_URL,
                decode_responses=True,
                max_connections=10,
                retry_on_timeout=True
            )
            self._redis.ping()
        return self._redis
    
    def close(self) -> None:
        """Close Redis connection"""
        if self._redis:
            self._redis.close()
            self._redis = None

redis_manager = RedisManager()
