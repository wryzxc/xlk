"""
用户学习行为追踪系统验证测试
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 70)
print('用户学习行为追踪系统验证')
print('=' * 70)

# 1. 管理员登录
r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)
print(f'\n[1] 管理员登录: {r.status_code}')

# 2. 测试学习行为日志页面
r = session.get(f'{BASE}/admin/learning_logs', timeout=10)
print(f'[2] 学习行为日志页面: {r.status_code}')
text = r.text
features = {
    '筛选功能': 'filter-bar' in text,
    '导出按钮': '导出CSV' in text,
    '分页组件': 'pagination' in text,
    '数据表格': 'log-table' in text,
    '类型筛选': 'logType' in text,
    '用户筛选': 'userId' in text,
}
for name, ok in features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 3. 测试课程观看记录页面
r = session.get(f'{BASE}/admin/lesson_views', timeout=10)
print(f'\n[3] 课程观看记录页面: {r.status_code}')
text = r.text
features = {
    '用户筛选': 'userId' in text,
    '课程筛选': 'courseId' in text,
    '导出按钮': '导出CSV' in text,
    '完成状态': 'status-badge' in text,
    '数据表格': 'data-table' in text,
}
for name, ok in features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 4. 测试练习尝试记录页面
r = session.get(f'{BASE}/admin/exercise_attempts', timeout=10)
print(f'\n[4] 练习尝试记录页面: {r.status_code}')
text = r.text
features = {
    '状态筛选': 'status' in text,
    '练习筛选': 'exerciseId' in text,
    '得分显示': 'score' in text,
    '代码预览': 'code_submitted' in text,
    '数据表格': 'data-table' in text,
}
for name, ok in features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 5. 测试考试参与记录页面
r = session.get(f'{BASE}/admin/exam_participations', timeout=10)
print(f'\n[5] 考试参与记录页面: {r.status_code}')
text = r.text
features = {
    '通过筛选': 'passed' in text,
    '正确率显示': 'correct_count' in text,
    '考试时间': 'started_at' in text,
    '导出功能': '导出CSV' in text,
    '数据表格': 'data-table' in text,
}
for name, ok in features.items():
    print(f'    {name}: {"OK" if ok else "FAIL"}')

# 6. 测试导出功能
exports = [
    ('学习日志导出', f'{BASE}/admin/export_logs'),
    ('课程观看导出', f'{BASE}/admin/export_lesson_views'),
    ('练习记录导出', f'{BASE}/admin/export_exercise_attempts'),
    ('考试记录导出', f'{BASE}/admin/export_exam_participations'),
]
print('\n[6] 数据导出功能:')
for name, url in exports:
    r = session.get(url, timeout=10)
    content_type = r.headers.get('Content-Type', '')
    ok = r.status_code == 200 and ('text/csv' in content_type or 'application/octet-stream' in content_type)
    print(f'    {name}: {"OK" if ok else "FAIL"} (status={r.status_code}, type={content_type})')

# 7. 检查数据库模型
print('\n[7] 数据库模型检查:')
import sys
sys.path.insert(0, r'e:\安装包\28\python-learning-platform')
from app import app, db, User, LearningLog, LessonViewLog, ExerciseAttemptLog, ExamParticipationLog
with app.app_context():
    models = {
        'LearningLog': LearningLog,
        'LessonViewLog': LessonViewLog,
        'ExerciseAttemptLog': ExerciseAttemptLog,
        'ExamParticipationLog': ExamParticipationLog,
    }
    for name, model in models.items():
        try:
            count = model.query.count()
            print(f'    {name}: OK (记录数: {count})')
        except Exception as e:
            print(f'    {name}: FAIL ({str(e)})')

print('\n' + '=' * 70)
print('验证完成！')
print('=' * 70)
