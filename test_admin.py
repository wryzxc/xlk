"""
管理员后台功能验证测试
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 70)
print('管理员后台功能验证')
print('=' * 70)

# 管理员登录
r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)
print(f'\n[1] 管理员登录: {r.status_code}')

# 访问管理后台
r = session.get(f'{BASE}/admin', timeout=10)
text = r.text
print(f'[2] 管理后台页面: {r.status_code}')

# 检查关键模块
modules = {
    '仪表盘': 'tab-dashboard',
    '用户管理': 'tab-users',
    '课程管理': 'tab-courses',
    '提交记录': 'tab-submissions',
    '操作日志': 'tab-logs',
    '统计报表': 'tab-reports',
}
print('\n[3] 模块检查:')
for name, tab_id in modules.items():
    found = f'id="{tab_id}"' in text
    print(f'    {name}: {"OK" if found else "FAIL"}')

# 检查统计数据 (Jinja2模板变量在渲染后会被替换为实际值)
stats = ['用户总数', '课程数量', '练习数量', '考试数量', '今日新增']
print('\n[4] 统计数据展示:')
for stat in stats:
    found = stat in text
    print(f'    {stat}: {"OK" if found else "FAIL"}')

# 检查图表
charts = ['submissionChart', 'activityChart', 'dauChart', 'passRateChart', 'examScoreChart']
print('\n[5] 图表组件:')
for chart in charts:
    found = f'id="{chart}"' in text
    print(f'    {chart}: {"OK" if found else "FAIL"}')

# 检查表格
tables = ['userTable', 'logContainer']
print('\n[6] 数据表格:')
for table in tables:
    found = f'id="{table}"' in text
    print(f'    {table}: {"OK" if found else "FAIL"}')

# 检查筛选功能
filters = ['userSearch', 'userRoleFilter', 'logSearch', 'logTypeFilter']
print('\n[7] 筛选功能:')
for f in filters:
    found = f'id="{f}"' in text
    print(f'    {f}: {"OK" if found else "FAIL"}')

# 检查Chart.js
print('\n[8] Chart.js库:', 'OK' if 'chart.js' in text else 'FAIL')

print('\n' + '=' * 70)
print('验证完成！')
print('=' * 70)
