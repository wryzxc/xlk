"""优化验证脚本 - 测试所有已实施的优化项"""
import requests
import sys

BASE_URL = 'http://127.0.0.1:5000'
results = []

# 创建会话并登录
session = requests.Session()
login_resp = session.post(f'{BASE_URL}/login', data={
    'username': 'admin',
    'password': 'admin123'
}, timeout=10, allow_redirects=True)
print(f'登录状态: {login_resp.status_code}')

def test(name, method, path, checks=None, data=None, use_session=False):
    """执行测试并验证响应"""
    try:
        url = f'{BASE_URL}{path}'
        req_session = session if use_session else requests
        if method == 'GET':
            resp = req_session.get(url, timeout=10)
        elif method == 'POST':
            resp = req_session.post(url, json=data, timeout=10)
        else:
            resp = req_session.request(method, url, timeout=10)

        status = resp.status_code == 200
        details = []

        if checks:
            for check_name, check_func in checks.items():
                try:
                    check_result = check_func(resp)
                    if not check_result:
                        status = False
                        details.append(f'{check_name}: FAIL')
                    else:
                        details.append(f'{check_name}: PASS')
                except Exception as e:
                    status = False
                    details.append(f'{check_name}: ERROR ({e})')

        results.append({
            'name': name,
            'status': 'PASS' if status else 'FAIL',
            'code': resp.status_code,
            'details': details
        })
        return resp
    except Exception as e:
        results.append({
            'name': name,
            'status': 'FAIL',
            'code': None,
            'details': [f'Exception: {e}']
        })
        return None

# ========== 测试开始 ==========

print('=' * 60)
print('Python编程实训平台 - 优化效果验证')
print('=' * 60)

# 1. 首页动态数据测试
print('\n[1] 首页动态统计数据...')
test('首页动态数据', 'GET', '/', {
    '包含动态课程数': lambda r: '6' in r.text and '系统课程' in r.text,
    '包含动态课时数': lambda r: '33' in r.text and '精选课时' in r.text,
    '包含动态练习数': lambda r: '99' in r.text and '编程练习' in r.text,
    '包含动态考试数': lambda r: '3' in r.text and '分级考试' in r.text,
})

# 2. SEO基础测试
print('[2] SEO Meta标签...')
test('SEO Meta标签', 'GET', '/', {
    '包含OG标题': lambda r: 'og:title' in r.text,
    '包含OG描述': lambda r: 'og:description' in r.text,
    '包含Twitter Card': lambda r: 'twitter:card' in r.text,
    '包含Canonical': lambda r: 'canonical' in r.text,
    '包含Keywords': lambda r: 'meta name="keywords"' in r.text,
})

# 3. 安全响应头测试
print('[3] 安全响应头...')
resp = test('安全响应头', 'GET', '/', {
    'X-Content-Type-Options': lambda r: r.headers.get('X-Content-Type-Options') == 'nosniff',
    'X-Frame-Options': lambda r: r.headers.get('X-Frame-Options') == 'SAMEORIGIN',
    'Referrer-Policy': lambda r: 'strict-origin-when-cross-origin' in (r.headers.get('Referrer-Policy') or ''),
    'Permissions-Policy': lambda r: 'geolocation=()' in (r.headers.get('Permissions-Policy') or ''),
})

# 4. Sitemap测试
print('[4] Sitemap生成...')
test('Sitemap', 'GET', '/sitemap.xml', {
    'XML格式正确': lambda r: '<?xml' in r.text and '<urlset' in r.text,
    '包含首页': lambda r: '<loc>' in r.text and '</loc>' in r.text,
    '包含课程页面': lambda r: '/course/' in r.text,
})

# 5. Robots.txt测试
print('[5] Robots.txt...')
test('Robots.txt', 'GET', '/robots.txt', {
    '包含User-agent': lambda r: 'User-agent:' in r.text,
    '包含Sitemap引用': lambda r: 'Sitemap:' in r.text,
    '禁止后台': lambda r: 'Disallow: /admin/' in r.text,
})

# 6. 代码安全验证测试
print('[6] 代码执行安全沙箱...')

# 6.1 正常代码应该通过
resp = test('正常代码执行', 'POST', '/run_code', {
    '执行成功': lambda r: r.json().get('success') == True,
}, data={'code': 'print(2 + 3)'}, use_session=True)

# 6.2 危险代码应该被拦截
resp = test('拦截import os', 'POST', '/run_code', {
    '被拦截': lambda r: r.json().get('success') == False and '安全检查' in r.json().get('error', ''),
}, data={'code': 'import os'}, use_session=True)

# 6.3 eval应该被拦截
resp = test('拦截eval', 'POST', '/run_code', {
    '被拦截': lambda r: r.json().get('success') == False,
}, data={'code': 'eval("1+1")'}, use_session=True)

# 6.4 字符串拼接绕过应该被拦截
resp = test('拦截字符串拼接绕过', 'POST', '/run_code', {
    '被拦截': lambda r: r.json().get('success') == False,
}, data={'code': '__im' + 'port__("os")'}, use_session=True)

# 7. 练习页面CodeMirror测试
print('[7] 练习页面CodeMirror集成...')
test('练习页面编辑器', 'GET', '/exercise/1', {
    '包含CodeMirror CSS': lambda r: 'codemirror' in r.text.lower(),
    '包含CodeMirror JS': lambda r: 'codemirror.min.js' in r.text,
    '包含Python模式': lambda r: 'mode/python' in r.text,
    '包含Dracula主题': lambda r: 'dracula' in r.text.lower(),
    '包含本地草稿功能': lambda r: 'localStorage' in r.text,
}, use_session=True)

# ========== 结果汇总 ==========
print('\n' + '=' * 60)
print('验证结果汇总')
print('=' * 60)

passed = sum(1 for r in results if r['status'] == 'PASS')
failed = sum(1 for r in results if r['status'] == 'FAIL')
total = len(results)

for r in results:
    status_icon = '[PASS]' if r['status'] == 'PASS' else '[FAIL]'
    print(f"  {status_icon} {r['name']}: {r['status']} (HTTP {r['code']})")
    for d in r['details']:
        print(f"      - {d}")

print('-' * 60)
print(f'总计: {passed}/{total} 通过, {failed}/{total} 失败')
print(f'通过率: {passed/total*100:.1f}%')
print('=' * 60)

if failed > 0:
    sys.exit(1)
