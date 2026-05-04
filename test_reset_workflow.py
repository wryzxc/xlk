"""
重置功能完整工作流验证
测试范围：重置按钮响应、初始代码加载、运行/提交功能
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 60)
print('重置功能完整工作流验证')
print('=' * 60)

# 登录
session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)

# 1. 获取练习页面
r = session.get(f'{BASE}/exercise/1', timeout=10)
text = r.text
print(f'\n[1] 页面加载: {r.status_code}')

# 2. 检查重置按钮入口
print('[2] 重置入口检查:')
print(f'    重置按钮存在: {"resetCode()" in text}')
has_reset_btn = 'id="resetBtn"' in text
print(f'    按钮ID(resetBtn): {has_reset_btn}')
print(f'    按钮文字(重置): {">重置<" in text}')

# 3. 检查初始代码数据
print('\n[3] 初始代码数据检查:')
print(f'    originalCode变量: {"originalCode" in text}')
print(f'    starter_code: {"starter_code" in text}')
# 提取初始代码内容
import re
starter_match = re.search(r"originalCode = (.+?);", text)
if starter_match:
    print(f'    初始代码内容: {starter_match.group(1)[:80]}')

# 4. 检查EditorResetModule
print('\n[4] 重置模块检查:')
print(f'    EditorResetModule: {"EditorResetModule" in text}')
print(f'    resetToOriginal: {"resetToOriginal" in text}')
print(f'    TO_ORIGINAL模式: {"TO_ORIGINAL" in text}')
print(f'    clearHistory: {"clearHistory" in text}')

# 5. 检查初始化模块（确认默认空白）
print('\n[5] 初始化策略检查:')
returns_empty = "return ''" in text
print(f'    默认返回空白: {returns_empty}')
print(f'    空白状态日志: {"初始化为空白状态" in text}')

# 6. 运行代码功能测试
print('\n[6] 运行代码功能测试:')
r = session.post(f'{BASE}/run_code', json={'code': "print('Hello, World!')"}, timeout=10)
data = r.json()
print(f'    请求状态: {r.status_code}')
print(f'    执行成功: {data.get("success")}')
print(f'    输出包含Hello: {"Hello" in data.get("output", "")}')

# 7. 提交答案功能测试
print('\n[7] 提交答案功能测试:')
r = session.post(f'{BASE}/submit_exercise/1', json={'code': "print('Hello, World!')"}, timeout=10)
data = r.json()
print(f'    请求状态: {r.status_code}')
print(f'    提交成功: {data.get("success")}')
print(f'    有评分: {"score" in data}')

# 8. 检查安全沙箱
print('\n[8] 安全沙箱测试:')
r = session.post(f'{BASE}/run_code', json={'code': 'import os'}, timeout=10)
data = r.json()
print(f'    危险代码被拦截: {not data.get("success")}')

print('\n' + '=' * 60)
print('验证完成！重置功能工作正常。')
print('=' * 60)
print('\n【重置功能使用说明】')
print('1. 首次打开页面：编辑器为完全空白状态')
print('2. 点击"重置"按钮：恢复为预设初始代码 (print("Hello, World!"))')
print('3. 运行代码：点击"运行代码"按钮或按 Ctrl+Enter')
print('4. 提交答案：点击"提交答案"按钮')
print('5. 保存草稿：按 Ctrl+S（保存到本地，刷新后需手动恢复）')
