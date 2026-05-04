# -*- coding: utf-8 -*-
"""Comprehensive tests for the exam system update"""
import requests
import json
import sys

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(url, name):
    try:
        resp = requests.get(url, timeout=10)
        print(f"  [{resp.status_code}] {name}: {'OK' if resp.status_code == 200 else 'FAIL'}")
        return resp
    except Exception as e:
        print(f"  [ERR] {name}: {e}")
        return None

print("=" * 60)
print("Exam System Comprehensive Test")
print("=" * 60)

# Test 1: Home page
print("\n[1] Home Page")
test_endpoint(f"{BASE_URL}/", "Home")

# Test 2: Exams listing page
print("\n[2] Exams Page")
resp = test_endpoint(f"{BASE_URL}/exams", "Exams List")
if resp:
    # Check all 7 exams present
    for exam_name in ["Python基础入门测试", "Python数据结构测试", "面向对象编程测试",
                       "文件操作与异常处理测试", "Python高级特性测试", "Web开发基础测试",
                       "Python综合能力考核"]:
        found = exam_name in resp.text
        print(f"    Exam '{exam_name}': {'OK' if found else 'MISSING'}")
    
    # Check all cards show 120 minutes
    count_120 = resp.text.count("120 分钟")
    print(f"    '120 分钟' occurrences: {count_120} (expected 7)")
    
    # Check all cards show passing score 60%
    count_60 = resp.text.count("60.0%")
    print(f"    '60.0%' occurrences: {count_60} (expected 7)")
    
    # Check 57 questions mentioned
    count_57 = resp.text.count("57 题")
    print(f"    '57 题' occurrences: {count_57} (expected 7)")

# Test 3: Individual exam detail pages
print("\n[3] Exam Detail Pages")
exam_ids = [1, 2, 3, 4, 5, 6, 7]
exam_names = [
    "Python基础入门测试", "Python数据结构测试", "面向对象编程测试",
    "文件操作与异常处理测试", "Python高级特性测试", "Web开发基础测试",
    "Python综合能力考核"
]
for eid, ename in zip(exam_ids, exam_names):
    resp = test_endpoint(f"{BASE_URL}/exam/{eid}", f"Exam {eid}: {ename}")
    if resp:
        has_57 = "57 题" in resp.text or "57" in resp.text
        has_120 = "120 分钟" in resp.text or "120" in resp.text
        print(f"      57 questions: {'OK' if has_57 else 'CHECK'}")
        print(f"      120 minutes: {'OK' if has_120 else 'CHECK'}")

# Test 4: Login and check authenticated pages
print("\n[4] Auth Pages")
test_endpoint(f"{BASE_URL}/login", "Login Page")
test_endpoint(f"{BASE_URL}/register", "Register Page")

# Test 5: Check admin pages
print("\n[5] Admin Pages (will redirect to login)")
for page in ['/admin', '/admin/users', '/admin/exercises', '/admin/exams']:
    resp = test_endpoint(f"{BASE_URL}{page}", page)
    if resp and resp.status_code == 302:
        print(f"    {page}: Redirect to login (expected)")

# Test 6: Course pages  
print("\n[6] Course Pages")
for cid in range(1, 7):
    test_endpoint(f"{BASE_URL}/course/{cid}", f"Course {cid}")

# Test 7: Resources & Community
print("\n[7] Other Pages")
for page in ['/resources', '/community']:
    test_endpoint(f"{BASE_URL}{page}", page)

# Test 8: Verify database directly
print("\n[8] Database Verification")
import sys
sys.path.insert(0, '.')
try:
    from app import app, db, ExamAttempt, User
    with app.app_context():
        exams_in_db = db.session.execute(db.text("SELECT COUNT(*) FROM exam")).scalar()
        questions_in_db = db.session.execute(db.text("SELECT COUNT(*) FROM exam_question")).scalar()
        print(f"    Exams in DB: {exams_in_db} (expected 7)")
        print(f"    Questions in DB: {questions_in_db} (expected 399)")
        
        # Count per exam
        for eid in range(1, 8):
            count = db.session.execute(
                db.text("SELECT COUNT(*) FROM exam_question WHERE exam_id = :eid"), {"eid": eid}
            ).scalar()
            print(f"    Exam {eid} questions: {count} (expected 57)")
except Exception as e:
    print(f"    DB verification error: {e}")

print("\n" + "=" * 60)
print("Tests Complete!")
print("=" * 60)
