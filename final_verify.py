# -*- coding: utf-8 -*-
"""Final comprehensive verification of all exam system updates"""
import requests
import re
from collections import Counter

print("=" * 65)
print("  FINAL COMPREHENSIVE VERIFICATION")
print("=" * 65)

# ===== 1. EXAMS PAGE DISPLAY =====
print("\n[1] EXAMS PAGE DISPLAY")
resp = requests.get("http://127.0.0.1:5000/exams")
html = resp.text

exam_names = [
    "Python基础入门测试", "Python数据结构测试", "面向对象编程测试",
    "文件操作与异常处理测试", "Python高级特性测试", "Web开发基础测试",
    "Python综合能力考核"
]
checks = {
    "All 7 exams present": all(n in html for n in exam_names),
    "'57 题' × 7": html.count("57 题") == 7,
    "'120 分钟' × 7": html.count("120 分钟") == 7,
    "'60.0%' × 7": html.count("60.0%") == 7,
    "Unified description format": html.count("涵盖单选题30题、判断题10题、填空题8题、程序阅读题4题、简答题3题、编程题2题，总分100分，限时120分钟") >= 6,
    "Progress bar present": "progress" in html.lower(),
}
for name, result in checks.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")

# ===== 2. DATABASE VERIFICATION =====
print("\n[2] DATABASE VERIFICATION")
import sys
sys.path.insert(0, '.')
from app import app, db

with app.app_context():
    n_exams = db.session.execute(db.text("SELECT COUNT(*) FROM exam")).scalar()
    n_q = db.session.execute(db.text("SELECT COUNT(*) FROM exam_question")).scalar()
    
    print(f"  Exams: {n_exams}/7  Questions: {n_q}/399")
    
    all_ok = True
    for eid in range(1, 8):
        count = db.session.execute(
            db.text("SELECT COUNT(*) FROM exam_question WHERE exam_id=:eid"), {"eid": eid}
        ).scalar()
        types = db.session.execute(
            db.text("SELECT question_type, COUNT(*) FROM exam_question WHERE exam_id=:eid GROUP BY 1"),
            {"eid": eid}
        ).fetchall()
        type_map = dict(types)
        expected = {'single_choice': 30, 'true_false': 10, 'fill_blank': 8,
                    'code_reading': 4, 'short_answer': 3, 'programming': 2}
        type_ok = type_map == expected
        if not type_ok: all_ok = False
        print(f"  Exam {eid}: {count} questions [{'OK' if type_ok else 'MISMATCH'}]")
    
    print(f"  Type distribution: {'ALL MATCH' if all_ok else 'MISMATCH DETECTED'}")

# ===== 3. EXAM CONFIG VERIFICATION =====
print("\n[3] EXAM CONFIG PARAMETERS")
with app.app_context():
    exams = db.session.execute(db.text(
        "SELECT title, duration_minutes, passing_score, level FROM exam ORDER BY id"
    )).fetchall()
    
    for exam in exams:
        d_ok = exam[1] == 120
        p_ok = exam[2] == 60.0
        print(f"  {exam[0]}: duration={exam[1]}min {'OK' if d_ok else 'FAIL'}, "
              f"passing={exam[2]}% {'OK' if p_ok else 'FAIL'}, level={exam[3]}")

# ===== 4. ALL PAGES ACCESSIBLE =====
print("\n[4] ALL PAGES ACCESSIBLE")
pages = [
    ("Home", "/"),
    ("Exams", "/exams"),
    ("Courses", "/courses"),
    ("Resources", "/resources"),
    ("Community", "/community"),
    ("Login", "/login"),
    ("Register", "/register"),
]
for name, path in pages:
    r = requests.get(f"http://127.0.0.1:5000{path}")
    print(f"  [{r.status_code}] {name}: {'OK' if r.status_code == 200 else 'FAIL'}")

# ===== 5. EXAM DETAIL PAGES (auth required, check redirect) =====
print("\n[5] EXAM DETAIL PAGES (redirects to login, expected)")
for eid in range(1, 8):
    r = requests.get(f"http://127.0.0.1:5000/exam/{eid}", allow_redirects=False)
    redirects_to_login = r.status_code in (302, 301)
    print(f"  Exam {eid}: {'Redirects' if redirects_to_login else 'Status ' + str(r.status_code)}")

# ===== 6. STATIC ASSETS =====
print("\n[6] STATIC ASSETS")
for asset in ["/static/css/main.min.css", "/static/js/main.min.js", "/static/js/i18n.js"]:
    r = requests.get(f"http://127.0.0.1:5000{asset}")
    print(f"  [{r.status_code}] {asset}: {'OK' if r.status_code == 200 else 'FAIL'}")

print("\n" + "=" * 65)
print("  VERIFICATION COMPLETE")
print("=" * 65)
