#!/bin/bash

# Render 构建脚本

echo "开始构建..."

# 安装依赖
pip install -r requirements.txt

# 创建上传目录
mkdir -p uploads

# 初始化数据库（如果数据库文件不存在）
if [ ! -f "platform.db" ]; then
    echo "初始化数据库..."
    python -c "
import os
os.environ['FLASK_ENV'] = 'production'
from app import app, db
from init_db import init_database
with app.app_context():
    db.create_all()
    init_database()
"
    echo "数据库初始化完成"
else
    echo "数据库已存在，跳过初始化"
fi

echo "构建完成"
