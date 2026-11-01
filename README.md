# 星辰科技公司网站

> Vue3 + TypeScript + Naive UI 前端 | FastAPI + Redis + MySQL + MongoDB 后端

公司宣传网站，支持后台动态修改公司信息、图片、产品、新闻等内容。

---

## 技术栈

### 前端

| 技术         | 说明                                      |
| ------------ | ----------------------------------------- |
| Vue 3        | 渐进式框架，使用`<script setup>` 语法糖 |
| TypeScript   | 类型安全                                  |
| Naive UI     | Vue3 组件库                               |
| Vue Router 4 | 路由管理，history 工作模式                |
| Axios        | HTTP 请求                                 |
| Vite         | 构建工具                                  |

**响应式 API**：`ref`、`reactive`、`computed`、`onMounted`、`watch`

### 后端

| 技术           | 说明                                 |
| -------------- | ------------------------------------ |
| FastAPI        | 异步 Web 框架                        |
| SQLAlchemy 2.0 | MySQL ORM                            |
| PyMySQL        | MySQL 驱动                           |
| Redis          | 缓存（公司信息、产品列表、新闻列表） |
| Motor          | MongoDB 异步驱动（存储联系表单）     |
| Pydantic v2    | 数据校验                             |

**数据库分工**：

- **MySQL**：公司信息、产品、新闻、团队成员（结构化数据）
- **MongoDB**：联系表单消息（文档型数据）
- **Redis**：缓存层，减轻数据库查询压力

---

## 目录结构

```
.
├── frontend/                  # 前端工程
│   ├── src/
│   │   ├── api/               # API 请求层
│   │   │   ├── request.ts     # Axios 封装
│   │   │   ├── company.ts     # 公司信息接口
│   │   │   ├── product.ts     # 产品接口
│   │   │   ├── news.ts        # 新闻接口
│   │   │   └── contact.ts     # 联系表单接口
│   │   ├── components/        # 公共组件
│   │   │   ├── AppHeader.vue  # 顶部导航
│   │   │   ├── AppFooter.vue  # 页脚
│   │   │   └── SectionTitle.vue # 区块标题
│   │   ├── composables/       # 组合式函数
│   │   │   └── useCompanyData.ts # 数据获取与兜底
│   │   ├── router/
│   │   │   └── index.ts       # 路由配置 (history 模式)
│   │   ├── types/
│   │   │   └── index.ts       # TypeScript 类型定义
│   │   ├── views/             # 页面视图
│   │   │   ├── HomeView.vue   # 首页
│   │   │   ├── AboutView.vue  # 关于我们
│   │   │   ├── ProductView.vue # 产品服务
│   │   │   ├── NewsView.vue   # 新闻动态
│   │   │   └── ContactView.vue # 联系我们
│   │   ├── App.vue            # 根组件
│   │   └── main.ts            # 入口文件
│   ├── index.html
│   ├── vite.config.ts         # Vite 配置 (含代理)
│   ├── tsconfig.json
│   └── package.json
│
├── backend/                   # 后端工程
│   ├── app/
│   │   ├── api/
│   │   │   ├── deps.py        # 依赖注入
│   │   │   └── v1/            # 路由
│   │   │       ├── company.py # 公司信息路由
│   │   │       ├── product.py # 产品路由
│   │   │       ├── news.py    # 新闻路由
│   │   │       └── contact.py # 联系表单路由
│   │   ├── core/
│   │   │   └── config.py      # 应用配置（标题/版本/CORS）
│   │   ├── schemas/           # Pydantic 模型
│   │   │   ├── company.py
│   │   │   ├── product.py
│   │   │   ├── news.py
│   │   │   └── contact.py
│   │   ├── services/          # 业务逻辑层
│   │   │   ├── company_service.py
│   │   │   ├── product_service.py
│   │   │   ├── news_service.py
│   │   │   └── contact_service.py
│   │   └── main.py            # FastAPI 入口
│   ├── requirements.txt       # 应用运行依赖
│   └── .env                   # 应用配置（标题/版本/CORS）
│
├── db/                        # 独立数据库层（与 backend 同级）
│   ├── config.py              # 数据库配置（MySQL/Redis/MongoDB）
│   ├── .env                   # 数据库连接配置（随 db 包存放）
│   ├── core/
│   │   ├── mysql_db.py        # MySQL 连接
│   │   ├── redis_client.py    # Redis 客户端
│   │   └── mongo_db.py        # MongoDB 连接
│   ├── models/
│   │   └── mysql/             # SQLAlchemy 模型
│   │       ├── company.py     # Company, TeamMember
│   │       ├── product.py     # Product
│   │       └── news.py        # News
│   └── scripts/
│       └── init_db.py         # 数据库初始化脚本
│
├── docker-compose.yml
└── README.md
```

---

## 快速开始

### 前提条件

- Node.js >= 18
- Python >= 3.10
- MySQL >= 8.0
- Redis >= 6.0
- MongoDB >= 5.0

### 1. 启动前端

```bash
cd frontend
npm install
npm run dev
```

前端运行在 `http://localhost:5173`，未启动后端时自动使用内置兜底数据。

### 2. 启动后端

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt -r ../db/requirements.txt
```

### 3. 配置数据库

数据库连接配置已迁移到独立 db 包的 `db/.env`（与 backend 同级），修改其中的连接信息即可：

```ini
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DATABASE=stellar_tech

REDIS_HOST=127.0.0.1
REDIS_PORT=6379

MONGO_HOST=127.0.0.1
MONGO_PORT=27017
```

应用级配置（标题/版本/CORS）位于 `backend/.env`。

先在 MySQL 中创建数据库：

```sql
CREATE DATABASE stellar_tech CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 4. 初始化数据

db 包位于项目根目录，请在项目根目录执行：

```bash
python -m db.scripts.init_db
```

脚本会自动创建表并写入种子数据（公司信息、团队、产品、新闻）。

### 5. 启动后端服务

db 包位于项目根目录，运行后端时需把项目根加入 `PYTHONPATH`。

Windows PowerShell：

```powershell
cd backend
$env:PYTHONPATH = ".."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Linux / macOS：

```bash
cd backend
PYTHONPATH=.. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 文档：`http://localhost:8000/docs`
- ReDoc：`http://localhost:8000/redoc`

---

## API 接口概览

| 方法   | 路径                         | 说明                               |
| ------ | ---------------------------- | ---------------------------------- |
| GET    | `/api/company/info`        | 获取公司信息                       |
| PUT    | `/api/company/info`        | 更新公司信息                       |
| GET    | `/api/company/team`        | 获取团队成员                       |
| POST   | `/api/company/team`        | 新增团队成员                       |
| GET    | `/api/products`            | 获取产品列表（可选 category 筛选） |
| GET    | `/api/products/{id}`       | 获取产品详情                       |
| POST   | `/api/products`            | 新增产品                           |
| PUT    | `/api/products/{id}`       | 更新产品                           |
| DELETE | `/api/products/{id}`       | 删除产品                           |
| GET    | `/api/news`                | 获取新闻列表（分页）               |
| GET    | `/api/news/{id}`           | 获取新闻详情                       |
| POST   | `/api/news`                | 新增新闻                           |
| PUT    | `/api/news/{id}`           | 更新新闻                           |
| DELETE | `/api/news/{id}`           | 删除新闻                           |
| POST   | `/api/contact`             | 提交联系表单                       |
| GET    | `/api/contact`             | 获取联系消息列表                   |
| PUT    | `/api/contact/{id}/status` | 更新消息状态                       |

---

## 缓存策略

| Redis Key                              | TTL   | 说明         |
| -------------------------------------- | ----- | ------------ |
| `company:info`                       | 3600s | 公司信息缓存 |
| `company:team`                       | 3600s | 团队成员缓存 |
| `products:list:{category}`           | 3600s | 产品列表缓存 |
| `product:detail:{id}`                | 3600s | 产品详情缓存 |
| `news:list:{category}:{page}:{size}` | 3600s | 新闻列表缓存 |
| `news:detail:{id}`                   | 3600s | 新闻详情缓存 |

数据变更时自动清除对应缓存。

---

## 前后端联调说明

前端 Vite 配置了代理，`/api` 请求会转发到 `http://127.0.0.1:8000`。

如果后端未启动，前端会使用 `useCompanyData.ts` 中的默认数据兜底，页面正常展示。

---

## 部署说明

### 前端构建

```bash
cd frontend
npm run build
```

产物在 `frontend/dist/`，部署到 Nginx 等 Web 服务器。

Nginx 需配置 history 模式回退：

```nginx
location / {
    try_files $uri $uri/ /index.html;
}

location /api {
    proxy_pass http://127.0.0.1:8000;
}
```

### 后端部署

```bash
cd backend
pip install -r requirements.txt -r ../db/requirements.txt
# 需把项目根加入 PYTHONPATH，以便导入同级 db 包
PYTHONPATH=.. uvicorn app.main:app --host 0.0.0.0 --port 8000
```

建议使用 `gunicorn` + `uvicorn` worker 生产部署：

```bash
cd backend
PYTHONPATH=.. gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```
