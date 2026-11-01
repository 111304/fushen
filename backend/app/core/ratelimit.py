"""基于 Redis 的固定窗口限流工具"""

import time

from fastapi import HTTPException, Request

from db.core.redis_client import redis_client


def get_client_ip(request: Request) -> str:
    """获取客户端真实 IP

    请求经 nginx 反代后 request.client.host 是 nginx 的内网地址，
    所有访客会共享同一个 IP，必须优先取 X-Forwarded-For 的首个地址
    （nginx.conf 已配置 proxy_set_header X-Forwarded-For）。
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def _hit(key: str, limit: int, window_seconds: int) -> bool:
    """固定窗口计数：窗口内第 limit 次及之前返回 True，之后 False

    Redis INCR 原子自增，首次命中时给键设置窗口长度的过期时间，
    窗口自然滚动，无需额外清理任务。
    """
    window_id = int(time.time()) // window_seconds
    cache_key = f"ratelimit:{key}:{window_id}"

    count = redis_client.incr(cache_key)
    if count == 1:
        redis_client.client.expire(cache_key, window_seconds)
    return count <= limit


def check_contact_rate_limit(request: Request) -> None:
    """联系表单限流：每 IP 60 秒 1 条，每天 10 条，超限抛 429"""
    ip = get_client_ip(request)

    if not _hit(f"contact:min:{ip}", limit=1, window_seconds=60):
        raise HTTPException(status_code=429, detail="提交太频繁，请稍后再试")

    if not _hit(f"contact:day:{ip}", limit=10, window_seconds=86400):
        raise HTTPException(status_code=429, detail="今日提交次数已达上限，请明日再试或直接致电联系我们")
