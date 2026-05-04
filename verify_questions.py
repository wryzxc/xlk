# -*- coding: utf-8 -*-
import re
from collections import Counter

content = open('course_data.py', 'r', encoding='utf-8').read()

# Count questions by exam and type
pattern = r'"exam":(\d+),.*?"type":"([^"]+)"'
matches = re.findall(pattern, content)

exams = Counter()
types = Counter()
for exam_id, qtype in matches:
    exams[exam_id] += 1
    types[qtype] += 1

print(f"Total questions: {len(matches)}")
print(f"\nPer exam:")
for k in sorted(exams.keys(), key=int):
    print(f"  Exam {k}: {exams[k]} questions")

print(f"\nPer type:")
for k, v in sorted(types.items()):
    print(f"  {k}: {v}")

print(f"\nExpected per exam: 57")
print(f"Expected total (exams 1-6 + 7): {6*57 + 57} = 399")

# Check exam 7 is intact
exam7_count = sum(1 for m in matches if m[0] == '7')
print(f"\nExam 7 questions: {exam7_count}")
