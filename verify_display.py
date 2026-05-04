# -*- coding: utf-8 -*-
"""Final verification: exams page content check"""
import requests
import re

resp = requests.get("http://127.0.0.1:5000/exams")
html = resp.text

print("=" * 60)
print("FINAL VERIFICATION: Exams Page Display")
print("=" * 60)

# 1. Check all exam cards present
exam_titles = [
    "Python基础入门测试", "Python数据结构测试", "面向对象编程测试",
    "文件操作与异常处理测试", "Python高级特性测试", "Web开发基础测试",
    "Python综合能力考核"
]
all_present = all(t in html for t in exam_titles)
print(f"\n[1] All 7 exam titles present: {'PASS' if all_present else 'FAIL'}")

# 2. Check question count: 57题 for each
count_57 = len(re.findall(r'题目数量.*?57', html))
# Look more broadly
count_57_full = html.count('57 题')
print(f"[2] '57 题' count: {count_57_full} (expected 7): {'PASS' if count_57_full == 7 else 'FAIL'}")

# 3. Check exam duration: 120分钟 for each
count_120 = html.count('120 分钟')
print(f"[3] '120 分钟' count: {count_120} (expected 7): {'PASS' if count_120 == 7 else 'FAIL'}")

# 4. Check passing score: 60% for each  
count_60 = html.count('60.0%')
print(f"[4] '60.0%' count: {count_60} (expected 7): {'PASS' if count_60 == 7 else 'FAIL'}")

# 5. Check unified description format
desc_formats = [
    "涵盖单选题30题、判断题10题、填空题8题、程序阅读题4题、简答题3题、编程题2题，总分100分，限时120分钟"
]
for desc in desc_formats:
    count_desc = html.count(desc)
    print(f"[5] Unified description count: {count_desc} (expected 6-7): {'PASS' if count_desc >= 6 else 'FAIL'}")

# 6. Print exam card summaries from HTML
print(f"\n[6] Extracted exam card summaries:")
cards = re.findall(r'<h3[^>]*>(.*?)</h3>.*?<p[^>]*>(.*?)</p>.*?题目数量.*?(\d+).*?考试时长.*?(\d+)', html, re.DOTALL)
for title, desc, qcount, duration in cards:
    print(f"    {title}: {qcount}题, {duration}分钟")
    desc_short = desc[:80].strip()
    print(f"      Desc: {desc_short}...")

# 7. Check progress bar reference
print(f"\n[7] Progress bar references: ", end="")
if 'progress' in html.lower():
    print("PASS (found)")
else:
    print("CHECK (not found)")

print("\n" + "=" * 60)
print("ALL CHECKS COMPLETE")
print("=" * 60)
