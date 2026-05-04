import sqlite3
conn = sqlite3.connect('instance/platform.db')
c = conn.cursor()

print('=' * 60)
print('考试系统数据验证')
print('=' * 60)

# 考试数量
c.execute('SELECT COUNT(*) FROM exam')
print(f'\n考试总数: {c.fetchone()[0]}')

# 题目数量
c.execute('SELECT COUNT(*) FROM exam_question')
print(f'题目总数: {c.fetchone()[0]}')

# 各考试题目数
c.execute('''SELECT exam.title, COUNT(exam_question.id) 
             FROM exam LEFT JOIN exam_question ON exam.id = exam_question.exam_id 
             GROUP BY exam.id ORDER BY exam.id''')
print('\n各考试题目数:')
for row in c.fetchall():
    print(f'  - {row[0]}: {row[1]} 题')

# 题型分布
c.execute('SELECT question_type, COUNT(*) FROM exam_question GROUP BY question_type')
print('\n题型分布:')
for row in c.fetchall():
    print(f'  - {row[0]}: {row[1]} 题')

# 难度分布（通过分值推断）
c.execute('''SELECT 
    CASE 
        WHEN points = 3 THEN '简单'
        WHEN points = 5 THEN '中等'
        WHEN points = 8 THEN '困难'
        ELSE '其他'
    END as difficulty,
    COUNT(*) 
    FROM exam_question 
    GROUP BY difficulty''')
print('\n难度分布:')
for row in c.fetchall():
    print(f'  - {row[0]}: {row[1]} 题')

# 各考试总分
c.execute('''SELECT exam.title, SUM(exam_question.points) 
             FROM exam LEFT JOIN exam_question ON exam.id = exam_question.exam_id 
             GROUP BY exam.id ORDER BY exam.id''')
print('\n各考试总分:')
for row in c.fetchall():
    print(f'  - {row[0]}: {row[1]} 分')

conn.close()
print('\n' + '=' * 60)
print('验证完成！')
