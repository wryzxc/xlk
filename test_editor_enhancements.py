"""
代码编辑器增强功能验证测试
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 70)
print('代码编辑器增强功能验证')
print('=' * 70)

# 登录
r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)
print(f'\n[1] 登录: {r.status_code}')

# 获取练习页面
r = session.get(f'{BASE}/exercise/1', timeout=10)
text = r.text
print(f'[2] 练习页面: {r.status_code}')

# 一、基础编辑核心功能
print('\n[3] 基础编辑核心功能:')
basic_features = {
    'CodeMirror编辑器': 'CodeMirror' in text,
    'Python语法高亮': 'codemirror-python' in text,
    '自动闭合括号': 'codemirror-closebrackets' in text,
    '括号匹配': 'codemirror-matchbrackets' in text,
    '当前行高亮': 'codemirror-activeline' in text,
    '代码折叠': 'foldGutter' in text,
    '行号显示': 'lineNumbers' in text,
    '查找替换对话框': 'searchDialog' in text,
    '重置按钮': 'resetCode()' in text,
    '清空按钮': 'clearCode()' in text,
}
for name, ok in basic_features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 二、交互体验优化
print('\n[4] 交互体验优化:')
ux_features = {
    '设置面板': 'settingsPanel' in text,
    '主题切换': 'themeSelect' in text,
    '字体大小调整': 'fontSizeSelect' in text,
    '缩进设置': 'indentSizeSelect' in text,
    '行高设置': 'lineHeightSelect' in text,
    '自动保存': 'autoSaveSelect' in text,
    'Vim/Emacs模式': 'keyMapSelect' in text,
    '专注模式': 'toggleFocusMode' in text,
    '明暗主题': 'light-theme' in text,
}
for name, ok in ux_features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 三、性能优化
print('\n[5] 性能优化:')
perf_features = {
    '虚拟滚动(viewportMargin)': 'viewportMargin' in text,
    '行包装(lineWrapping)': 'lineWrapping' in text,
}
for name, ok in perf_features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 四、快捷键
print('\n[6] 键盘快捷键:')
shortcuts = {
    'Ctrl+Enter运行': 'Ctrl-Enter' in text,
    'Ctrl+S保存': 'Ctrl-S' in text,
    'Ctrl+F查找': 'Ctrl-F' in text,
    'Ctrl+H替换': 'Ctrl-H' in text,
    'F11专注模式': 'F11' in text,
    'Esc关闭对话框': 'Esc' in text,
}
for name, ok in shortcuts.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 五、输出区域
print('\n[7] 输出区域:')
output_features = {
    '输出面板': 'output-card' in text,
    '加载动画': 'spinner' in text,
    '成功样式': 'output-success' in text,
    '错误样式': 'output-error' in text,
    '清除按钮': 'clearOutput' in text,
}
for name, ok in output_features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 六、Toast通知
print('\n[8] Toast通知系统:')
toast_features = {
    'Toast容器': 'toast-container' in text,
    '成功样式': 'toast.success' in text,
    '错误样式': 'toast.error' in text,
    '警告样式': 'toast.warning' in text,
}
for name, ok in toast_features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 统计
all_checks = list(basic_features.values()) + list(ux_features.values()) + list(perf_features.values()) + list(shortcuts.values()) + list(output_features.values()) + list(toast_features.values())
passed = sum(all_checks)
total = len(all_checks)

print('\n' + '=' * 70)
print(f'验证结果: {passed}/{total} 项通过 ({passed/total*100:.1f}%)')
print('=' * 70)

if passed == total:
    print('\n所有编辑器增强功能验证通过！')
else:
    print(f'\n有 {total - passed} 项功能需要检查。')
