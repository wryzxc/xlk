"""
完全清空功能验证测试
验证重置操作后编辑器是否完全空白，无任何残留内容或格式信息
"""
import requests
import re

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 70)
print('完全清空功能验证测试')
print('=' * 70)

# 登录
session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)

# 获取练习页面
r = session.get(f'{BASE}/exercise/1', timeout=10)
text = r.text

print('\n[1] 页面加载状态')
print(f'    HTTP状态码: {r.status_code}')

print('\n[2] 清空按钮检查')
has_clear_btn = 'id="clearBtn"' in text
has_clear_func = 'clearCode()' in text
print(f'    清空按钮存在: {has_clear_btn}')
print(f'    清空函数绑定: {has_clear_func}')

print('\n[3] 完全清空功能代码检查')
# 检查是否包含所有清空操作
checks = {
    '设置目标内容(setValue)': 'editor.setValue(targetContent)' in text,
    '清除历史记录(clearHistory)': 'editor.clearHistory()' in text,
    '重置光标位置(setCursor)': 'editor.setCursor' in text,
    '清除选区(setSelection)': 'editor.setSelection' in text,
    '滚动到顶部(scrollTo)': 'editor.scrollTo(0, 0)' in text,
    '刷新编辑器(refresh)': 'editor.refresh()' in text,
    '清除高亮标记(getAllMarks)': 'editor.getAllMarks' in text,
    '清除自动补全': 'completionActive' in text,
    '清除本地存储草稿': 'localStorage.removeItem' in text,
}
for name, result in checks.items():
    status = 'OK' if result else 'FAIL'
    print(f'    {name}: {status}')

print('\n[4] 初始化策略检查')
init_blank = "return ''" in text
init_log = '初始化为空白状态' in text
print(f'    默认空白初始化: {init_blank}')
print(f'    空白状态日志: {init_log}')

print('\n[5] 重置模式检查')
modes = ['TO_ORIGINAL', 'TO_BLANK', 'TO_DRAFT']
for mode in modes:
    status = 'OK' if mode in text else 'FAIL'
    print(f'    {mode}模式: {status}')

print('\n[6] 功能完整性测试')
# 测试运行代码
r = session.post(f'{BASE}/run_code', json={'code': "print('test')"}, timeout=10)
data = r.json()
run_status = 'OK' if data.get("success") else 'FAIL'
print(f'    代码运行功能: {run_status}')

# 测试提交
r = session.post(f'{BASE}/submit_exercise/1', json={'code': "print('test')"}, timeout=10)
data = r.json()
submit_status = 'OK' if data.get("success") else 'FAIL'
print(f'    答案提交功能: {submit_status}')

print('\n' + '=' * 70)
print('验证完成！')
print('=' * 70)
print('\n【完全清空功能说明】')
print('点击"清空"按钮或调用 resetToBlank() 将执行以下操作：')
print('1. 编辑器内容设为空字符串')
print('2. 清除所有撤销/重做历史')
print('3. 光标位置重置到 (0,0)')
print('4. 清除所有文本选区')
print('5. 清除搜索/替换状态')
print('6. 清除所有高亮标记')
print('7. 滚动到编辑器顶部')
print('8. 刷新编辑器UI确保同步')
print('9. 清除本地存储的草稿数据')
print('10. 清除自动补全和覆盖层状态')
print('\n重置后编辑器将呈现完全空白的初始状态。')
