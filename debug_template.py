import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

# 先注册一个测试用户
r = session.post(f'{BASE}/register', data={
    'username': 'testuser2',
    'email': 'test2@test.com',
    'password': 'test123'
}, timeout=10)
print(f'Register: {r.status_code}')

# 登录
r = session.post(f'{BASE}/login', data={
    'username': 'testuser2',
    'password': 'test123'
}, timeout=10)
print(f'Login: {r.status_code}')

# 获取练习页面
r = session.get(f'{BASE}/exercise/1', timeout=10)
print(f'Exercise page: {r.status_code}')
print(f'Content length: {len(r.text)}')

# 检查关键内容
keywords = ['CodeMirror', 'codemirror', 'toast', 'settingsPanel', 'searchDialog', 
            'focus-mode', 'editor', 'originalCode', 'exerciseId']
for kw in keywords:
    print(f'Contains "{kw}": {kw in r.text}')

# 查找可能的问题
if 'Traceback' in r.text or 'Error' in r.text:
    print('\n--- Error found in page ---')
    # 找到错误部分
    idx = r.text.find('Traceback')
    if idx == -1:
        idx = r.text.find('Error')
    print(r.text[idx:idx+500])
