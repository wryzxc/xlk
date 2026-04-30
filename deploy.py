#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EdgeOne Pages 部署脚本
用于自动化部署前的环境检查和配置验证
"""

import os
import sys
import subprocess
import json

def check_python_version():
    """检查 Python 版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("[ERROR] Python 版本需要 >= 3.10，当前版本: {}.{}".format(version.major, version.minor))
        return False
    print("[OK] Python 版本: {}.{}.{}".format(version.major, version.minor, version.micro))
    return True

def check_dependencies():
    """检查依赖包"""
    print("\n[检查] 依赖包安装状态...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        missing = []
        for req in requirements:
            package = req.split('==')[0]
            try:
                __import__(package.lower().replace('flask-', 'flask_'))
            except ImportError:
                missing.append(req)
        
        if missing:
            print("[WARN] 缺少以下依赖包:")
            for pkg in missing:
                print("  - {}".format(pkg))
            print("[提示] 运行: pip install -r requirements.txt")
            return False
        else:
            print("[OK] 所有依赖包已安装")
            return True
    except FileNotFoundError:
        print("[ERROR] requirements.txt 文件不存在")
        return False

def check_environment_variables():
    """检查环境变量"""
    print("\n[检查] 环境变量配置...")
    required_vars = ['SECRET_KEY']
    optional_vars = ['DATABASE_URL']
    
    missing_required = []
    for var in required_vars:
        if not os.environ.get(var):
            missing_required.append(var)
    
    if missing_required:
        print("[WARN] 缺少必要环境变量:")
        for var in missing_required:
            print("  - {}".format(var))
        print("[提示] 生产环境必须设置这些变量")
    else:
        print("[OK] 必要环境变量已配置")
    
    for var in optional_vars:
        if os.environ.get(var):
            print("[OK] 可选变量 {} 已设置".format(var))
        else:
            print("[INFO] 可选变量 {} 未设置，将使用默认值".format(var))
    
    return True

def check_file_structure():
    """检查项目文件结构"""
    print("\n[检查] 项目文件结构...")
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/base.html',
        'static/css/main.min.css',
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(file):
            missing.append(file)
    
    if missing:
        print("[ERROR] 缺少必要文件:")
        for f in missing:
            print("  - {}".format(f))
        return False
    else:
        print("[OK] 项目文件结构完整")
        return True

def check_database():
    """检查数据库状态"""
    print("\n[检查] 数据库状态...")
    db_path = 'instance/platform.db'
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print("[OK] SQLite 数据库存在 (大小: {:.2f} KB)".format(size / 1024))
        return True
    else:
        print("[WARN] SQLite 数据库不存在")
        print("[提示] 运行: python init_db.py 初始化数据库")
        return False

def generate_deployment_package():
    """生成部署包"""
    print("\n[操作] 生成部署包...")
    
    # 创建部署目录
    deploy_dir = 'deploy'
    if not os.path.exists(deploy_dir):
        os.makedirs(deploy_dir)
    
    # 复制必要文件
    import shutil
    files_to_copy = [
        'app.py',
        'requirements.txt',
        'init_db.py',
        'course_data.py',
        'course_enhancements.py',
        'wrangler.toml',
        '_worker.js',
        '.pages.yml',
    ]
    
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, deploy_dir)
            print("  [OK] 复制 {}".format(file))
    
    # 复制目录
    dirs_to_copy = ['templates', 'static']
    for dir_name in dirs_to_copy:
        if os.path.exists(dir_name):
            dest = os.path.join(deploy_dir, dir_name)
            if os.path.exists(dest):
                shutil.rmtree(dest)
            shutil.copytree(dir_name, dest)
            print("  [OK] 复制 {} 目录".format(dir_name))
    
    print("[OK] 部署包已生成到 {} 目录".format(deploy_dir))
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("EdgeOne Pages 部署前检查")
    print("=" * 60)
    
    checks = [
        check_python_version(),
        check_file_structure(),
        check_dependencies(),
        check_environment_variables(),
        check_database(),
    ]
    
    print("\n" + "=" * 60)
    if all(checks):
        print("[成功] 所有检查通过，项目可以部署")
        print("=" * 60)
        
        # 询问是否生成部署包
        response = input("\n是否生成部署包? (y/n): ").lower().strip()
        if response == 'y':
            generate_deployment_package()
        return 0
    else:
        print("[失败] 部分检查未通过，请修复后重试")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
