"""
学练考模块全面测试脚本
测试范围：练习页面（代码运行/提交/重置）、考试页面（单选/多选/填空）
"""
import requests
import sys

BASE = 'http://127.0.0.1:5000'
session = requests.Session()
results = []

def test(name, method, path, checks=None, data=None):
    try:
        url = f'{BASE}{path}'
        if method == 'GET':
            r = session.get(url, timeout=15)
        elif method == 'POST':
            r = session.post(url, json=data, timeout=15)
        else:
            r = session.request(method, url, timeout=15)

        ok = r.status_code == 200
        details = []
        if checks:
            for cname, cfunc in checks.items():
                try:
                    cok = cfunc(r)
                    if not cok:
                        ok = False
                        details.append(f'{cname}: FAIL')
                    else:
                        details.append(f'{cname}: PASS')
                except Exception as e:
                    ok = False
                    details.append(f'{cname}: ERROR ({e})')

        results.append({'name': name, 'status': 'PASS' if ok else 'FAIL', 'code': r.status_code, 'details': details})
        return r
    except Exception as e:
        results.append({'name': name, 'status': 'FAIL', 'code': None, 'details': [f'Exception: {e}']})
        return None

print('=' * 65)
print('学练考模块全面测试')
print('=' * 65)

# 1. 登录
print('\n[1] 用户登录...')
login_r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10, allow_redirects=True)
print(f'    登录状态: {login_r.status_code}')
if login_r.status_code != 200:
    print('    登录失败，终止测试')
    sys.exit(1)

# ========== 练习页面测试 ==========
print('\n[2] 练习页面 - 基础加载...')
test('练习页面加载', 'GET', '/exercise/1', {
    '页面正常加载': lambda r: r.status_code == 200,
    '包含CodeMirror CSS': lambda r: 'codemirror' in r.text.lower(),
    '包含CodeMirror JS': lambda r: 'codemirror.min.js' in r.text,
    '包含Python模式': lambda r: 'codemirror-python' in r.text,
    '包含Dracula主题': lambda r: 'dracula' in r.text.lower(),
    '包含运行按钮': lambda r: 'id="runCodeBtn"' in r.text,
    '包含提交按钮': lambda r: 'id="submitCodeBtn"' in r.text,
    '包含重置按钮': lambda r: 'resetCode()' in r.text,
    '编辑器高度400px': lambda r: 'height: 400px' in r.text,
    '包含本地草稿功能': lambda r: 'localStorage' in r.text,
    '包含键盘快捷键': lambda r: 'Ctrl-Enter' in r.text,
    '输出区域存在': lambda r: 'id="output"' in r.text,
    '清除按钮存在': lambda r: 'clearOutput()' in r.text,
})

print('[3] 练习页面 - 代码运行功能...')
test('正常代码运行', 'POST', '/run_code', {
    '请求成功': lambda r: r.status_code == 200,
    '返回JSON': lambda r: r.headers.get('Content-Type', '').startswith('application/json'),
    '执行成功': lambda r: r.json().get('success') == True,
    '有输出内容': lambda r: '5' in (r.json().get('output') or ''),
}, data={'code': 'print(2 + 3)'})

print('[4] 练习页面 - 代码提交功能...')
test('正常代码提交', 'POST', '/submit_exercise/1', {
    '请求成功': lambda r: r.status_code == 200,
    '返回JSON': lambda r: r.headers.get('Content-Type', '').startswith('application/json'),
    '提交成功': lambda r: r.json().get('success') == True,
    '有评分结果': lambda r: 'score' in r.json(),
}, data={'code': "print('Hello, World!')"})

print('[5] 练习页面 - 安全沙箱测试...')
test('拦截import os', 'POST', '/run_code', {
    '请求成功': lambda r: r.status_code == 200,
    '被拦截': lambda r: r.json().get('success') == False,
    '返回安全错误': lambda r: '安全检查' in (r.json().get('error') or ''),
}, data={'code': 'import os'})

test('拦截eval', 'POST', '/run_code', {
    '被拦截': lambda r: r.json().get('success') == False,
}, data={'code': 'eval("1+1")'})

test('拦截字符串拼接绕过', 'POST', '/run_code', {
    '被拦截': lambda r: r.json().get('success') == False,
}, data={'code': '__im' + 'port__("os")'})

# ========== 考试页面测试 ==========
print('\n[6] 考试页面 - 基础加载...')
test('考试页面加载', 'GET', '/exam/1', {
    '页面正常加载': lambda r: r.status_code == 200,
    '包含考试标题': lambda r: 'Python基础测试' in r.text or '在线考试' in r.text,
    '包含题目卡片': lambda r: 'question-card' in r.text,
    '包含答题进度': lambda r: 'exam-progress' in r.text,
    '包含快速导航': lambda r: 'nav-' in r.text,
    '包含提交按钮': lambda r: 'checkBeforeSubmit' in r.text,
})

print('[7] 考试页面 - 题型检查...')
# 获取考试页面内容分析题型
exam_r = session.get(f'{BASE}/exam/1', timeout=10)
if exam_r.status_code == 200:
    exam_text = exam_r.text
    
    # 检查单选题
    has_single = 'type="radio"' in exam_text
    print(f'    单选题选项: {"PASS" if has_single else "FAIL"} ({"找到radio" if has_single else "未找到radio"})')
    
    # 检查多选题
    has_multiple = 'type="checkbox"' in exam_text
    print(f'    多选题选项: {"PASS" if has_multiple else "FAIL"} ({"找到checkbox" if has_multiple else "未找到checkbox"})')
    
    # 检查填空题
    has_fillblank = 'fillblank-input' in exam_text
    print(f'    填空题输入框: {"PASS" if has_fillblank else "FAIL"} ({"找到输入框" if has_fillblank else "未找到输入框"})')
    
    # 检查题目类型标签
    has_type_badges = 'question-type-badge' in exam_text
    print(f'    题目类型标签: {"PASS" if has_type_badges else "FAIL"}')
    
    # 检查进度更新JS
    has_progress_js = 'updateProgress' in exam_text
    print(f'    进度更新脚本: {"PASS" if has_progress_js else "FAIL"}')
    
    # 检查选项点击交互
    has_select_option = 'selectOption' in exam_text
    print(f'    选项点击交互: {"PASS" if has_select_option else "FAIL"}')
    
    results.append({
        'name': '考试题型完整性',
        'status': 'PASS' if (has_single and has_multiple and has_fillblank) else 'FAIL',
        'code': 200,
        'details': [
            f'单选: {"PASS" if has_single else "FAIL"}',
            f'多选: {"PASS" if has_multiple else "FAIL"}',
            f'填空: {"PASS" if has_fillblank else "FAIL"}',
            f'类型标签: {"PASS" if has_type_badges else "FAIL"}',
            f'进度JS: {"PASS" if has_progress_js else "FAIL"}',
            f'选项交互: {"PASS" if has_select_option else "FAIL"}',
        ]
    })
else:
    results.append({
        'name': '考试题型完整性',
        'status': 'FAIL',
        'code': exam_r.status_code,
        'details': ['页面加载失败']
    })

# ========== 结果汇总 ==========
print('\n' + '=' * 65)
print('测试结果汇总')
print('=' * 65)

passed = sum(1 for r in results if r['status'] == 'PASS')
failed = sum(1 for r in results if r['status'] == 'FAIL')
total = len(results)

for r in results:
    icon = '[PASS]' if r['status'] == 'PASS' else '[FAIL]'
    print(f'  {icon} {r["name"]} (HTTP {r["code"]})')
    for d in r.get('details', []):
        print(f'      - {d}')

print('-' * 65)
print(f'总计: {passed}/{total} 通过, {failed}/{total} 失败')
print(f'通过率: {passed/total*100:.1f}%')
print('=' * 65)

if failed > 0:
    print('\n存在失败的测试项，请检查修复。')
    sys.exit(1)
else:
    print('\n所有测试通过！学练考模块功能正常。')
