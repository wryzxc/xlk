"""验证 exercises 页面修复"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

# 登录
session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)

print('=' * 50)
print('Exercises 页面修复验证')
print('=' * 50)

# 1. 测试基础页面
r = session.get(f'{BASE}/exercises', timeout=10)
print(f'\n[1] 基础页面: {r.status_code}')
print(f'    包含题目列表: {"练习题库" in r.text}')
print(f'    包含筛选器: {"category-filter" in r.text}')

# 2. 测试分类筛选
r = session.get(f'{BASE}/exercises?category=基础&difficulty=all', timeout=10)
print(f'\n[2] 分类筛选: {r.status_code}')
print(f'    页面正常: {r.status_code == 200}')

# 3. 测试难度筛选
r = session.get(f'{BASE}/exercises?category=all&difficulty=easy', timeout=10)
print(f'\n[3] 难度筛选: {r.status_code}')
print(f'    页面正常: {r.status_code == 200}')
print(f'    包含简单标签: {"简单" in r.text}')

# 4. 测试组合筛选
r = session.get(f'{BASE}/exercises?category=基础&difficulty=easy', timeout=10)
print(f'\n[4] 组合筛选: {r.status_code}')
print(f'    页面正常: {r.status_code == 200}')

print('\n' + '=' * 50)
print('验证完成！')
