# -*- coding: utf-8 -*-
"""Comprehensive test for sidebar toggle, visual cohesion, and button standardization"""
import requests

BASE = "http://127.0.0.1:5000"

def ok(test, name):
    status = "PASS" if test else "FAIL"
    print(f"  [{status}] {name}")
    return test

print("=" * 65)
print("  SIDEBAR TOGGLE + COHESION + BUTTONS — FINAL TEST")
print("=" * 65)

all_pass = True

# 1. Toggle button presence and styling
print("\n[1] TOGGLE BUTTON ENHANCEMENT")
resp = requests.get(f"{BASE}/")
html = resp.text

all_pass &= ok('sidebarToggle' in html, "Toggle button ID present")
all_pass &= ok('toggle-arrow' in html, "Toggle arrow element present")
all_pass &= ok('classList.toggle' in html, "Toggle JS logic present")
all_pass &= ok("localStorage.setItem('sidebar-collapsed'" in html, "State persistence present")
all_pass &= ok('aria-expanded' in html, "ARIA expanded attribute")
all_pass &= ok('aria-controls="sidebar"' in html, "ARIA controls relationship")
all_pass &= ok('Ctrl+B' in html or "ctrlKey" in html.lower(), "Ctrl+B keyboard shortcut")
all_pass &= ok('sidebar-toggle' in html.lower(), "Toggle CSS class defined")
all_pass &= ok('cubic-bezier' in html.lower(), "Custom easing curve present")
all_pass &= ok('sidebar-toggle' in html.lower() and 'width:32px' in html.lower(), "Toggle button 32px width")
all_pass &= ok('transform:scale' in html.lower(), "Scale animation on hover/active")

# 2. Visual cohesion - no hard borders
print("\n[2] VISUAL COHESION — Sidebar-Main Content")
all_pass &= ok('box-shadow:2px 0 16px' in html.lower(), "Soft sidebar shadow")
all_pass &= ok('border-right:1px solid' not in html.lower(), "No hard border-right")
all_pass &= ok('.main-wrapper' in html.lower(), "Main wrapper class present")
all_pass &= ok('var(--sidebar-transition)' in html.lower(), "Smooth transition variable")
all_pass &= ok('rgba(0,0,0,.06)' in html.lower(), "Subtle separator borders")
all_pass &= ok('border-top:1px solid rgba' in html.lower(), "Soft footer separator")
all_pass &= ok('::-webkit-scrollbar' in html.lower(), "Custom webkit scrollbar")
all_pass &= ok('scrollbar-width:thin' in html.lower(), "Firefox thin scrollbar")
all_pass &= ok('background:var(--bg-gray-50)' in html.lower(), "Content area gray background")

# 3. Button color standardization
print("\n[3] BUTTON COLOR STANDARDIZATION")

# Check index page hero buttons
r_idx = requests.get(f"{BASE}/")
idx_html = r_idx.text
all_pass &= ok('btn-primary' in idx_html, "Index: btn-primary class used")
all_pass &= ok('开始学习' in idx_html, "Index: 开始学习 present")
all_pass &= ok('开始练习' in idx_html, "Index: 开始练习 present")
all_pass &= ok('#8594' in idx_html, "Index: Arrow icon present")
all_pass &= ok('btn-outline-light' not in idx_html, "Index: No white outline button")
all_pass &= ok('btn-light' not in idx_html, "Index: No light bg button")

# Check exams page
r_exams = requests.get(f"{BASE}/exams")
exams_html = r_exams.text
all_pass &= ok('开始考试' in exams_html, "Exams: 开始考试 present")
all_pass &= ok('btn-primary' in exams_html, "Exams: btn-primary class")
all_pass &= ok('#8594' in exams_html, "Exams: Arrow icon present")

# Check exercises page
r_ex = requests.get(f"{BASE}/exercises")
ex_html = r_ex.text
all_pass &= ok('开始练习' in ex_html, "Exercises: 开始练习 present")
all_pass &= ok('btn-primary' in ex_html, "Exercises: btn-primary class")

# Check courses page
r_courses = requests.get(f"{BASE}/courses")
courses_html = r_courses.text
all_pass &= ok('开始学习' in courses_html, "Courses: 开始学习 present")
all_pass &= ok('btn-primary' in courses_html, "Courses: btn-primary class")

# 4. All pages load correctly
print("\n[4] ALL PAGES LOAD")
pages = [
    ("/", "Home"),
    ("/courses", "Courses"),
    ("/exercises", "Exercises"),
    ("/exams", "Exams"),
    ("/community", "Community"),
    ("/resources", "Resources"),
    ("/login", "Login"),
    ("/register", "Register"),
]
for path, name in pages:
    r = requests.get(f"{BASE}{path}", timeout=10)
    all_pass &= ok(r.status_code == 200, f"{name}: status={r.status_code}")

# 5. CSS verification
print("\n[5] CSS CONSISTENCY")
r_css = requests.get(f"{BASE}/static/css/main.min.css")
css = r_css.text
all_pass &= ok(".btn-primary" in css, "btn-primary CSS rule present")
all_pass &= ok("linear-gradient" in css, "Gradient background present")
all_pass &= ok("var(--primary)" in css, "Primary color variable present")
all_pass &= ok("margin-top:auto" in css, "Footer auto margin (sticky footer)")

# 6. Static assets
print("\n[6] STATIC ASSETS")
for a in ["/static/css/main.min.css", "/static/js/main.min.js", "/static/js/i18n.js"]:
    r = requests.get(f"{BASE}{a}")
    all_pass &= ok(r.status_code == 200, f"Asset: {a}")

print("\n" + "=" * 65)
print(f"  RESULT: {'ALL PASS' if all_pass else 'SOME FAILURES'}")
print("=" * 65)
exit(0 if all_pass else 1)
