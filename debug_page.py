import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

# 登录
r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)
print(f'Login: {r.status_code}')

# 获取练习页面
r = session.get(f'{BASE}/exercise/1', timeout=10)
print(f'Exercise page: {r.status_code}')
print(f'Content length: {len(r.text)}')
print(f'Contains "CodeMirror": {"CodeMirror" in r.text}')
print(f'Contains "codemirror": {"codemirror" in r.text.lower()}')
print(f'Contains "toast": {"toast" in r.text.lower()}')
print(f'Contains "settingsPanel": {"settingsPanel" in r.text}')
print(f'Contains "searchDialog": {"searchDialog" in r.text}')
print(f'Contains "focus-mode": {"focus-mode" in r.text}')

# 打印前500字符看看内容
print('\n--- First 500 chars ---')
print(r.text[:500])
print('\n--- Last 500 chars ---')
print(r.text[-500:])
