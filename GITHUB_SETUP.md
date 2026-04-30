# GitHub 仓库设置指南

## 当前状态

Git 仓库已初始化，代码已提交到本地 master 分支（55 个文件，15469 行代码）。

## 推送到 GitHub 的步骤

### 1. 在 GitHub 创建新仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `python-learning-platform`
   - Description: `Python编程实训平台 - 基于Flask的渐进式学习系统`
   - Visibility: Public（推荐）或 Private
   - 不要勾选 "Initialize this repository with a README"
3. 点击 **Create repository**

### 2. 关联本地仓库

GitHub 创建后会显示推送命令，在本地项目目录执行：

```bash
# 添加远程仓库地址（替换 YOUR_USERNAME 为你的 GitHub 用户名）
git remote add origin https://github.com/YOUR_USERNAME/python-learning-platform.git

# 验证远程仓库
git remote -v

# 推送到 GitHub（将本地 master 分支推送到远程）
git push -u origin master
```

### 3. 验证推送

```bash
# 查看提交历史
git log --oneline

# 查看远程分支
git branch -a
```

## 后续更新代码

```bash
# 查看修改状态
git status

# 添加修改的文件
git add .

# 提交修改
git commit -m "描述本次修改内容"

# 推送到 GitHub
git push origin master
```

## 项目文件说明

### 已提交的核心文件

| 文件/目录 | 说明 |
|-----------|------|
| `app.py` | Flask 应用主入口 |
| `requirements.txt` | Python 依赖列表 |
| `templates/` | HTML 模板文件（22个页面） |
| `static/` | 静态资源（CSS/JS） |
| `course_data.py` | 课程数据 |
| `course_enhancements.py` | 课程增强内容 |
| `init_db.py` | 数据库初始化脚本 |
| `deploy.py` | 部署检查脚本 |
| `wrangler.toml` | EdgeOne Pages 配置 |
| `.pages.yml` | Pages 部署配置 |
| `DEPLOY_GUIDE.md` | 部署指南 |

### 被排除的文件（.gitignore）

- `__pycache__/` - Python 缓存
- `instance/` - 本地数据库和配置
- `.env` - 环境变量（敏感信息）
- `test_*.py` - 测试脚本
- `*.db` - SQLite 数据库文件

## 分支管理建议

```bash
# 创建开发分支
git checkout -b develop

# 开发完成后合并到 master
git checkout master
git merge develop
git push origin master
```

## 协作开发

```bash
# 拉取最新代码
git pull origin master

# 创建功能分支
git checkout -b feature/new-feature

# 开发完成后提交 PR
git push origin feature/new-feature
# 然后在 GitHub 上创建 Pull Request
```

## 常见问题

### 推送被拒绝

```bash
# 如果远程仓库有更新，先拉取合并
git pull origin master --rebase
git push origin master
```

### 修改远程仓库地址

```bash
# 查看当前远程地址
git remote -v

# 修改远程地址
git remote set-url origin https://github.com/新用户名/新仓库名.git
```

### 配置 Git 用户信息

```bash
git config user.name "你的名字"
git config user.email "your@email.com"
```

## 下一步

1. 在 GitHub 创建仓库
2. 执行上面的推送命令
3. 在 GitHub 上查看代码
4. 配置 GitHub Actions（可选，用于自动部署）
