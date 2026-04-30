# EdgeOne Pages 项目部署指南

## 重要说明

**EdgeOne Pages 原生支持 Node.js 运行时，Python Flask 项目需要特殊部署方式。**

本项目提供三种部署方案：

| 方案 | 难度 | 成本 | 适用场景 |
|------|------|------|----------|
| **方案一：Workers + D1 数据库** | 中等 | 低 | 无服务器部署，自动扩缩容 |
| **方案二：Docker 容器部署** | 简单 | 中 | 需要完整 Python 环境 |
| **方案三：外部服务器 + Pages 前端** | 简单 | 中 | 已有服务器资源 |

---

## 方案一：EdgeOne Workers + D1 数据库（推荐）

### 1. 准备工作

```bash
# 安装 Wrangler CLI
npm install -g wrangler

# 登录 Cloudflare
wrangler login
```

### 2. 创建 D1 数据库

```bash
# 创建数据库
wrangler d1 create python-learning-db

# 记录返回的 database_id，更新到 wrangler.toml
```

### 3. 更新配置

编辑 `wrangler.toml`：

```toml
name = "xlk"
compatibility_date = "2024-01-01"

# D1 数据库绑定
[[d1_databases]]
binding = "DB"
database_name = "python-learning-db"
database_id = "your_database_id_here"
```

### 4. 初始化数据库

```bash
# 执行 SQL 初始化
wrangler d1 execute python-learning-db --file=./schema.sql
```

### 5. 部署

```bash
# 部署到 Workers
wrangler deploy

# 查看部署结果
wrangler tail
```

---

## 方案二：Docker 容器部署

### 1. 创建 Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 初始化数据库
RUN python init_db.py

EXPOSE 5000

CMD ["python", "app.py"]
```

### 2. 构建并推送镜像

```bash
# 构建镜像
docker build -t python-learning-platform .

# 推送到镜像仓库
docker tag python-learning-platform your-registry/python-learning-platform
docker push your-registry/python-learning-platform
```

### 3. 在 EdgeOne Pages 部署容器

在控制台选择 "容器部署"，配置镜像地址和环境变量。

---

## 方案三：外部服务器部署

### 1. 准备服务器

- 购买云服务器（阿里云/腾讯云/AWS等）
- 安装 Python 3.10+
- 安装 Nginx

### 2. 部署应用

```bash
# 克隆代码
git clone https://github.com/wryzxc/xlk.git
cd xlk

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py

# 使用 Gunicorn 运行
pip install gunicorn
gunicorn -w 4 -b 127.0.0.1:5000 app:app
```

### 3. Nginx 配置

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static/ {
        alias /path/to/xlk/static/;
        expires 30d;
    }
}
```

---

## 环境变量配置

无论哪种方案，都需要设置以下环境变量：

| 变量名 | 必填 | 说明 |
|--------|------|------|
| `SECRET_KEY` | 是 | Flask 密钥，用于会话加密 |
| `DATABASE_URL` | 否 | 数据库连接字符串 |
| `FLASK_ENV` | 否 | 运行环境（production/development） |

### 生成密钥

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 域名绑定

### 使用 EdgeOne 默认域名

部署成功后自动分配：
```
https://xlk.pages.dev
```

### 绑定自定义域名

1. 在控制台添加域名
2. 配置 DNS CNAME 记录指向 Pages 域名
3. 申请 SSL 证书（自动）

---

## 部署验证

```bash
# 测试首页
curl https://your-domain.com/

# 测试登录页
curl https://your-domain.com/login

# 检查响应头
curl -I https://your-domain.com/
```

---

## 常见问题

### Q: EdgeOne Pages 支持 Python 吗？
A: Pages 原生支持 Node.js。Python 项目建议使用 Workers 或容器部署。

### Q: 数据库怎么选择？
A: 
- 开发环境：SQLite
- 生产环境：D1（Serverless）、PostgreSQL、MySQL

### Q: 静态资源如何加速？
A: 使用 EdgeOne CDN，静态文件自动缓存到全球节点。

---

## 相关文档

- [EdgeOne Workers 文档](https://edgeone.ai/document/2145346)
- [D1 数据库文档](https://edgeone.ai/document/2145352)
- [Wrangler CLI 文档](https://edgeone.ai/document/2145350)
- [Flask 部署指南](https://flask.palletsprojects.com/en/3.0.x/deploying/)

---

**文档版本**: 2.0
**更新日期**: 2024-01-01
**项目**: xlk
