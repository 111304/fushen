"""Redis 连接客户端"""

import json
import redis
from typing import Any, Optional

from db.config import settings


class RedisClient:
    """Redis 缓存封装，支持 JSON 序列化"""

    def __init__(self):
        self._pool = redis.ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        self._client = redis.Redis(connection_pool=self._pool)

    @property
    def client(self) -> redis.Redis:
        return self._client

    def get_json(self, key: str) -> Optional[Any]:
        """获取 JSON 缓存"""
        val = self._client.get(key)
        if val is None:
            return None
        return json.loads(val)

    def set_json(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """写入 JSON 缓存"""
        data = json.dumps(value, ensure_ascii=False, default=str)
        self._client.set(key, data, ex=ttl or settings.cache_ttl)

    def delete(self, *keys: str) -> None:
        """删除缓存"""
        self._client.delete(*keys)

    def incr(self, key: str, amount: int = 1) -> int:
        """自增计数器"""
        return self._client.incr(key, amount)


redis_client = RedisClient()
