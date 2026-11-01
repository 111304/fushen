# ============================================================
#  星辰科技后端 - FastAPI 多阶段 Dockerfile
#  技术栈: Python 3.12 + FastAPI + Uvicorn
#  预估镜像大小: ~180MB
# ============================================================

# ===== Stage 1: Builder — 安装 Python 依赖 =====
FROM python:3.12.4-slim AS builder

# 设置工作目录
WORKDIR /build

# 换用清华 Debian 源（国内直连 deb.debian.org 太慢）并安装编译依赖
RUN sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
        /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 创建虚拟环境，隔离依赖；配置清华 PyPI 源加速
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV PIP_INDEX_URL="https://pypi.tuna.tsinghua.edu.cn/simple"

# 复制 backend 与 db 两套依赖，利用 Docker layer 缓存（context 为项目根目录）
COPY backend/requirements.txt backend/requirements.txt
COPY db/requirements.txt db/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r backend/requirements.txt -r db/requirements.txt


# ===== Stage 2: Runtime — 最小化运行时镜像 =====
FROM python:3.12.4-slim AS runtime

# 换用清华 Debian 源，安装运行时所需系统包（curl 用于健康检查）
RUN sed -i 's|http://deb.debian.org|https://mirrors.tuna.tsinghua.edu.cn|g' \
        /etc/apt/sources.list.d/debian.sources \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN groupadd -r appuser \
    && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# 从 builder 阶段复制虚拟环境
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

# 设置工作目录
WORKDIR /app

# 复制应用代码与独立 db 包（.dockerignore 会排除 .env、__pycache__ 等）
COPY --chown=appuser:appuser backend/ backend/
COPY --chown=appuser:appuser db/ db/

# 切换到非 root 用户
USER appuser

# 暴露 FastAPI 端口
EXPOSE 8000

# 健康检查 — FastAPI 根路由返回 {"status":"ok"}
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -sf http://127.0.0.1:8000/ || exit 1

# 启动命令
# 注意：项目代码采用扁平导入（from core.xxx / from api.xxx / from schemas.xxx），
# backend 的 app/ 目录作为扁平导入路径根，因此用 --app-dir /app/backend/app 指定模块搜索路径。
# 同时 db 包位于项目根（/app/db），需通过 PYTHONPATH=/app 暴露，否则报 ModuleNotFoundError。
ENV PYTHONPATH="/app"
CMD ["uvicorn", "main:app", "--app-dir", "/app/backend/app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
