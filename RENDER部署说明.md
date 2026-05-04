# Render 部署配置说明

## 已创建的文件

| 文件 | 用途 |
|------|------|
| `wsgi.py` | Gunicorn 入口文件 |
| `render.yaml` | Render 配置文件（可选，可用界面配置替代） |
| `build.sh` | 构建脚本（可选） |

## Render 界面配置步骤

根据你的截图，按以下方式填写：

### 1. 名称
```
python-learning-platform
```
（或你喜欢的名字，如 `py-learn`）

### 2. 语言
```
Python 3
```
（已自动识别，保持默认）

### 3. 分支
```
master
```
（或你的主分支名称，如 `main`）

### 4. 地区
```
新加坡 (新加坡)
```
（推荐选择亚洲节点，访问速度更快）

### 5. 根目录
```
（留空，使用仓库根目录）
```

### 6. 构建指令
```bash
pip install -r requirements.txt
```

### 7. 启动命令
```bash
gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 2 --timeout 60
```

### 8. 实例类型
```
免费
```
（512 MB 内存 / 0.1 CPU，适合业余项目）

---

## 环境变量设置（重要！）

点击 **高级** 或 **Environment** 标签，添加以下变量：

| 变量名 | 值 | 说明 |
|--------|-----|------|
| `SECRET_KEY` | （点击 Generate 自动生成） | 会话加密密钥 |
| `FLASK_ENV` | `production` | 生产环境模式 |
| `DATABASE_URL` | `sqlite:///platform.db` | 数据库路径 |

---

## 代码修改说明

### 1. `requirements.txt` 已添加 gunicorn
```
gunicorn==21.2.0
```

### 2. `wsgi.py` 入口文件
```python
import os
from app import app

if __name__ == "__main__":
    app.run()
```

### 3. `app.py` 无需修改
- 已支持环境变量读取 `SECRET_KEY` 和 `DATABASE_URL`
- SQLite 数据库文件会自动创建

---

## 部署后操作

### 首次部署后初始化数据

部署完成后，在 Render 控制台点击 **Shell**，运行：

```bash
python -c "
from app import app, db
from init_db import init_database
with app.app_context():
    db.create_all()
    init_database()
    print('数据初始化完成')
"
```

### 访问地址

部署成功后，访问：
```
https://your-service-name.onrender.com
```

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

---

## 注意事项

1. **免费实例休眠**：15分钟无访问会自动休眠，首次访问需等待唤醒（约30秒）
2. **数据库持久化**：SQLite 文件存储在磁盘上，重启后数据保留
3. **文件上传**：上传的文件也会保存在磁盘上
4. **日志查看**：在 Render 控制台点击 **Logs** 查看运行日志

---

## 重新部署

代码推送到 GitHub 后，Render 会自动重新部署。

或在 Render 控制台点击 **Manual Deploy** -> **Deploy latest commit**。
