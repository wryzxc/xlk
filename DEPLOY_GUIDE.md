# EdgeOne Pages 项目部署指南

## 目录

1. [项目概述](#1-项目概述)
2. [部署前准备](#2-部署前准备)
3. [配置文件说明](#3-配置文件说明)
4. [部署流程](#4-部署流程)
5. [环境变量配置](#5-环境变量配置)
6. [域名绑定](#6-域名绑定)
7. [部署后验证](#7-部署后验证)
8. [常见问题排查](#8-常见问题排查)
9. [最佳实践](#9-最佳实践)

---

## 1. 项目概述

本项目是一个基于 Flask 的 Python 编程学习平台，包含以下核心功能：

- 用户认证系统（注册/登录/权限管理）
- 课程体系管理（6门课程、33课时）
- 代码练习与在线评测
- 考试系统与成绩统计
- 学习进度追踪
- 管理员后台

### 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 运行时环境 |
| Flask | 3.0.0 | Web 框架 |
| Flask-SQLAlchemy | 3.1.1 | ORM 数据库 |
| Flask-Login | 0.6.3 | 用户会话管理 |
| SQLite | 3.x | 开发环境数据库 |

---

## 2. 部署前准备

### 2.1 系统要求

- **操作系统**: Windows 10/11, macOS 12+, 或 Linux (Ubuntu 20.04+)
- **Python**: 3.10 或更高版本
- **Node.js**: 18.x 或更高版本（用于 EdgeOne CLI）
- **Git**: 2.30+ 版本控制

### 2.2 安装 EdgeOne CLI

```bash
# 使用 npm 安装
npm install -g @edgeone/cli

# 验证安装
edgeone --version
```

### 2.3 项目准备

```bash
# 克隆项目（或准备本地项目）
git clone <your-repo-url> python-learning-platform
cd python-learning-platform

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 初始化数据库
python init_db.py
```

### 2.4 运行部署前检查

```bash
# 运行部署检查脚本
python deploy.py
```

检查脚本会验证：
- Python 版本 >= 3.10
- 项目文件结构完整性
- 依赖包安装状态
- 环境变量配置
- 数据库初始化状态

---

## 3. 配置文件说明

### 3.1 wrangler.toml

EdgeOne Pages 的主配置文件，定义项目构建和部署参数。

```toml
name = "python-learning-platform"
main = "app.py"
compatibility_date = "2024-01-01"

[build]
command = "pip install -r requirements.txt"

[env.production]
name = "python-learning-platform-prod"

[vars]
PYTHON_VERSION = "3.10"

[[rules]]
type = "CacheRule"
glob = "static/**/*"
ttl = 31536000

[[kv_namespaces]]
binding = "SESSION_KV"
id = "your_kv_namespace_id"

[[d1_databases]]
binding = "DB"
database_name = "python-learning-db"
database_id = "your_d1_database_id"
```

**关键配置项：**

| 配置项 | 说明 | 必填 |
|--------|------|------|
| `name` | 项目名称 | 是 |
| `main` | 入口文件 | 是 |
| `compatibility_date` | 兼容性日期 | 是 |
| `build.command` | 构建命令 | 是 |
| `kv_namespaces` | KV 存储（会话缓存） | 否 |
| `d1_databases` | D1 数据库（生产数据库） | 否 |

### 3.2 .pages.yml

EdgeOne Pages 高级配置，包含路由、缓存、头部设置等。

```yaml
build:
  command: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    python init_db.py
  environment:
    PYTHON_VERSION: "3.10"
    FLASK_ENV: "production"

deploy:
  entry: "app.py"
  runtime: "python"
  instance:
    memory: "512MB"
    timeout: "30s"

routes:
  - pattern: "/static/*"
    cache:
      ttl: 31536000
  - pattern: "/api/*"
    cache:
      ttl: 0
  - pattern: "/*"
    target: "app"

headers:
  - pattern: "/*"
    headers:
      X-Content-Type-Options: "nosniff"
      X-Frame-Options: "SAMEORIGIN"
```

### 3.3 _worker.js

Worker 脚本，用于处理静态资源缓存和安全头。

```javascript
export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    
    // 静态资源缓存策略
    if (url.pathname.startsWith('/static/')) {
      const response = await env.ASSETS.fetch(request);
      const headers = new Headers(response.headers);
      
      if (url.pathname.match(/\.(css|js)$/)) {
        headers.set('Cache-Control', 'public, max-age=31536000');
      }
      
      return new Response(response.body, {
        status: response.status,
        headers: headers
      });
    }
    
    return env.ASSETS.fetch(request);
  }
};
```

---

## 4. 部署流程

### 4.1 登录 EdgeOne 账户

```bash
# 使用 CLI 登录
edgeone login

# 或使用 API Token
edgeone login --token <your-api-token>
```

### 4.2 初始化项目

```bash
# 初始化 EdgeOne Pages 项目
edgeone pages project create

# 或关联现有项目
edgeone pages project link
```

### 4.3 配置构建命令

在 EdgeOne 控制台中设置构建命令：

```bash
# 构建命令
python -m pip install --upgrade pip && pip install -r requirements.txt && python init_db.py

# 输出目录
.

# 入口命令
python app.py
```

### 4.4 部署项目

#### 方式一：通过 CLI 部署

```bash
# 部署到预览环境
edgeone pages deploy

# 部署到生产环境
edgeone pages deploy --env production

# 使用特定分支部署
edgeone pages deploy --branch main
```

#### 方式二：通过 Git 集成自动部署

1. 在 EdgeOne 控制台关联 Git 仓库
2. 配置自动部署规则：
   - `main` 分支 -> 生产环境
   - `develop` 分支 -> 预览环境
3. 推送代码触发自动部署

```bash
# 推送代码触发部署
git add .
git commit -m "部署更新"
git push origin main
```

### 4.5 查看部署状态

```bash
# 查看部署日志
edgeone pages deployment list

# 查看实时日志
edgeone pages logs --tail

# 查看特定部署详情
edgeone pages deployment info <deployment-id>
```

---

## 5. 环境变量配置

### 5.1 必需环境变量

| 变量名 | 说明 | 示例值 |
|--------|------|--------|
| `SECRET_KEY` | Flask 密钥 | 随机生成的 32 位字符串 |
| `FLASK_ENV` | 运行环境 | `production` |

### 5.2 可选环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `DATABASE_URL` | 数据库连接 URL | `sqlite:///platform.db` |
| `SESSION_COOKIE_SECURE` | 安全 Cookie | `True` |
| `MAX_CONTENT_LENGTH` | 最大上传大小 | `16MB` |

### 5.3 设置环境变量

#### 通过 CLI 设置

```bash
# 设置密钥
edgeone pages secret put SECRET_KEY
# 输入密钥值: your-secret-key-here

# 设置数据库 URL
edgeone pages secret put DATABASE_URL
# 输入: sqlite:///platform.db
```

#### 通过控制台设置

1. 登录 [EdgeOne 控制台](https://console.edgeone.ai)
2. 进入项目 -> 设置 -> 环境变量
3. 添加键值对

### 5.4 生成安全密钥

```bash
# Python 生成随机密钥
python -c "import secrets; print(secrets.token_hex(32))"

# 或使用 openssl
openssl rand -hex 32
```

---

## 6. 域名绑定

### 6.1 使用 EdgeOne 默认域名

部署成功后，项目会自动分配默认域名：

```
https://python-learning-platform.pages.dev
```

### 6.2 绑定自定义域名

#### 步骤 1：添加域名

```bash
# 通过 CLI 添加域名
edgeone pages domain add www.yourdomain.com
```

#### 步骤 2：配置 DNS

在域名注册商处添加 DNS 记录：

| 类型 | 主机记录 | 记录值 | TTL |
|------|----------|--------|-----|
| CNAME | www | python-learning-platform.pages.dev | 600 |
| A | @ | EdgeOne 提供的 IP | 600 |

#### 步骤 3：验证域名

```bash
# 检查域名解析
dig www.yourdomain.com

# 或 nslookup
nslookup www.yourdomain.com
```

#### 步骤 4：配置 HTTPS

EdgeOne Pages 自动提供 SSL 证书：

1. 在控制台 -> 域名管理 -> 申请 SSL 证书
2. 等待证书自动颁发（通常 5-15 分钟）
3. 强制 HTTPS 跳转（推荐开启）

### 6.3 域名配置示例

```yaml
# .pages.yml 域名配置
domains:
  - domain: "www.yourdomain.com"
    https: true
    www_redirect: true
  - domain: "yourdomain.com"
    https: true
    redirect_to: "www.yourdomain.com"
```

---

## 7. 部署后验证

### 7.1 基础功能检查清单

- [ ] 首页正常加载
- [ ] 用户注册功能
- [ ] 用户登录功能
- [ ] 课程列表显示
- [ ] 课程详情页面
- [ ] 课时内容显示
- [ ] 代码编辑器加载
- [ ] 代码运行功能
- [ ] 考试系统
- [ ] 管理员后台

### 7.2 性能验证

```bash
# 测试首页加载速度
curl -o /dev/null -s -w "%{time_total}\n" https://your-domain.com/

# 预期结果: < 2秒
```

### 7.3 安全验证

```bash
# 检查安全响应头
curl -I https://your-domain.com/

# 预期输出:
# X-Content-Type-Options: nosniff
# X-Frame-Options: SAMEORIGIN
# Referrer-Policy: strict-origin-when-cross-origin
```

### 7.4 自动化测试脚本

```bash
# 运行自动化验证
python -c "
import requests

base_url = 'https://your-domain.com'
checks = [
    ('/', '首页'),
    ('/courses', '课程中心'),
    ('/login', '登录页'),
]

for path, name in checks:
    resp = requests.get(base_url + path, timeout=10)
    status = 'OK' if resp.status_code == 200 else 'FAIL'
    print(f'{name}: HTTP {resp.status_code} [{status}]')
"
```

---

## 8. 常见问题排查

### 8.1 构建失败

**问题**: `ModuleNotFoundError: No module named 'flask'`

**解决**:
```bash
# 确认 requirements.txt 存在
cat requirements.txt

# 手动安装依赖
pip install -r requirements.txt

# 重新部署
edgeone pages deploy
```

### 8.2 数据库错误

**问题**: `sqlite3.OperationalError: no such table`

**解决**:
```bash
# 本地初始化数据库后提交
python init_db.py
git add instance/platform.db
git commit -m "Add initialized database"
git push
```

### 8.3 静态资源 404

**问题**: CSS/JS 文件加载失败

**解决**:
1. 检查 `static` 目录是否在项目根目录
2. 确认 `wrangler.toml` 中静态资源规则
3. 检查文件路径大小写（Linux 区分大小写）

### 8.4 会话丢失

**问题**: 登录后状态不保持

**解决**:
```bash
# 检查 SECRET_KEY 是否设置
edgeone pages secret list

# 设置持久化密钥
edgeone pages secret put SECRET_KEY
```

### 8.5 环境变量未生效

**问题**: 配置的环境变量读取不到

**解决**:
1. 确认变量名拼写正确
2. 重新部署使变量生效
3. 检查代码中读取方式：`os.environ.get('VAR_NAME')`

### 8.6 性能问题

**问题**: 页面加载缓慢

**优化方案**:
1. 启用静态资源缓存
2. 使用 CDN 加速
3. 优化数据库查询
4. 启用 Gzip 压缩

```python
# app.py 中添加压缩
from flask_compress import Compress
Compress(app)
```

---

## 9. 最佳实践

### 9.1 安全建议

1. **密钥管理**
   - 使用强随机密钥
   - 定期轮换密钥
   - 不在代码中硬编码

2. **数据库安全**
   - 生产环境使用 D1 或外部数据库
   - 定期备份数据
   - 启用数据库加密

3. **访问控制**
   - 配置 IP 白名单
   - 启用 WAF 防护
   - 设置速率限制

### 9.2 性能优化

1. **缓存策略**
   - 静态资源长期缓存
   - API 响应适当缓存
   - 使用 KV 存储会话

2. **代码优化**
   - 数据库查询优化
   - 模板预编译
   - 懒加载非关键资源

### 9.3 监控告警

```bash
# 配置日志收集
edgeone pages logs --tail --format json

# 设置告警规则
edgeone pages alert create \
  --name "high-error-rate" \
  --condition "error_rate > 5%" \
  --notify "email:admin@example.com"
```

### 9.4 备份策略

1. **数据库备份**
   ```bash
   # 导出 SQLite 数据库
   sqlite3 instance/platform.db ".backup backup.db"
   ```

2. **配置备份**
   ```bash
   # 备份配置文件
   cp wrangler.toml wrangler.toml.backup
   cp .pages.yml .pages.yml.backup
   ```

---

## 附录

### A. 快速部署命令参考

```bash
# 完整部署流程
edgeone login
edgeone pages project create --name python-learning-platform
edgeone pages secret put SECRET_KEY
edgeone pages deploy

# 查看部署状态
edgeone pages deployment list
edgeone pages logs --tail
```

### B. 环境变量模板

```bash
# .env 文件模板（不要提交到 Git）
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///platform.db
FLASK_ENV=production
SESSION_COOKIE_SECURE=true
```

### C. 相关链接

- [EdgeOne Pages 文档](https://edgeone.ai/document/2145346)
- [EdgeOne CLI 参考](https://edgeone.ai/document/2145350)
- [Flask 部署指南](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [D1 数据库文档](https://edgeone.ai/document/2145352)

---

**文档版本**: 1.0
**更新日期**: 2024-01-01
**作者**: Python Learning Platform Team
