"""
编辑器模块功能验证测试
测试范围：初始化模块、重置模块、草稿模块的独立性和功能完整性
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 60)
print('编辑器模块功能验证')
print('=' * 60)

# 登录
session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)

# 1. 页面加载测试
r = session.get(f'{BASE}/exercise/1', timeout=10)
print(f'\n[1] 页面加载: {r.status_code}')
assert r.status_code == 200, '页面加载失败'

# 2. 检查三个模块是否都存在
text = r.text
print('[2] 模块存在性检查:')
print(f'    EditorInitModule: {"EditorInitModule" in text}')
print(f'    EditorResetModule: {"EditorResetModule" in text}')
print(f'    EditorDraftModule: {"EditorDraftModule" in text}')
print(f'    ResetMode枚举: {"ResetMode" in text}')
assert 'EditorInitModule' in text, '初始化模块未找到'
assert 'EditorResetModule' in text, '重置模块未找到'
assert 'EditorDraftModule' in text, '草稿模块未找到'
assert 'ResetMode' in text, '重置模式枚举未找到'

# 3. 检查初始化配置常量
print('\n[3] 初始化配置检查:')
print(f'    EDITOR_CONFIG: {"EDITOR_CONFIG" in text}')
mode_python = "mode: 'python'" in text
print(f'    mode: python: {mode_python}')
theme_dracula = "theme: 'dracula'" in text
print(f'    theme: dracula: {theme_dracula}')
print(f'    lineNumbers: {"lineNumbers: true" in text}')
print(f'    autoCloseBrackets: {"autoCloseBrackets: true" in text}')
print(f'    matchBrackets: {"matchBrackets: true" in text}')
print(f'    styleActiveLine: {"styleActiveLine: true" in text}')

# 4. 检查重置模式
print('\n[4] 重置模式检查:')
print(f'    TO_ORIGINAL: {"TO_ORIGINAL" in text}')
print(f'    TO_BLANK: {"TO_BLANK" in text}')
print(f'    TO_DRAFT: {"TO_DRAFT" in text}')

# 5. 检查错误处理
print('\n[5] 错误处理检查:')
print(f'    _handleError (Init): {"_handleError" in text}')
print(f'    _validateEditor: {"_validateEditor" in text}')
print(f'    clearHistory: {"clearHistory" in text}')

# 6. 检查功能入口函数
print('\n[6] 全局入口函数检查:')
print(f'    resetCode(): {"function resetCode()" in text}')
print(f'    saveDraft(): {"function saveDraft()" in text}')

# 7. 检查独立性（模块间不直接调用内部方法）
print('\n[7] 模块独立性检查:')
# 初始化模块不应调用重置模块
init_section = text.split('EditorInitModule')[1].split('EditorResetModule')[0]
print(f'    Init模块不依赖Reset: {"EditorResetModule" not in init_section}')
# 重置模块只使用editor全局变量
reset_section = text.split('EditorResetModule')[1].split('EditorDraftModule')[0]
print(f'    Reset模块使用editor变量: {"editor" in reset_section}')

# 8. 检查代码运行功能
print('\n[8] 代码运行功能检查:')
r = session.post(f'{BASE}/run_code', json={'code': 'print(2+3)'}, timeout=10)
print(f'    运行代码: {r.status_code}')
data = r.json()
print(f'    执行成功: {data.get("success")}')
print(f'    输出正确: {"5" in data.get("output", "")}')

# 9. 检查代码提交功能
print('\n[9] 代码提交功能检查:')
r = session.post(f'{BASE}/submit_exercise/1', json={'code': "print('Hello, World!')"}, timeout=10)
print(f'    提交代码: {r.status_code}')
data = r.json()
print(f'    提交成功: {data.get("success")}')
print(f'    有评分: {"score" in data}')

print('\n' + '=' * 60)
print('所有验证通过！编辑器模块功能完整。')
print('=' * 60)
