# ============================================================
#  星辰科技前端 - Vue 3 多阶段 Dockerfile
#  技术栈: Node 20 + Vite 5 + Vue 3 + TypeScript
#  预估镜像大小: ~30MB (Nginx Alpine)
# ============================================================

# ===== Stage 1: Builder — 编译前端静态资源 =====
FROM node:20.15.1-alpine AS builder

# 构建期环境变量（.env 已被 .dockerignore 排除，需在构建时注入）
# 可通过 --build-arg VITE_API_BASE_URL=xxx 覆盖
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

WORKDIR /build

# 先复制 package.json + lockfile，利用 layer 缓存
COPY package.json package-lock.json ./

# 确定性安装依赖
RUN npm ci

# 复制源代码并构建（.dockerignore 排除 node_modules、dist 等）
COPY . .

# 构建生产包，输出到 dist/
RUN npm run build


# ===== Stage 2: Runtime — Nginx 提供静态服务 =====
FROM nginx:1.27.1-alpine AS runtime

# 移除默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义 Nginx 配置（SPA 路由 + API 反向代理）
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 从 builder 阶段复制构建产物
COPY --from=builder /build/dist /usr/share/nginx/html

# 暴露 HTTP 端口
EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD wget -q --spider http://localhost/ || exit 1

# 启动 Nginx（前台运行）
CMD ["nginx", "-g", "daemon off;"]
