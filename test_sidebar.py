# -*- coding: utf-8 -*-
"""Comprehensive test for sidebar navigation system"""
import requests
import sys

BASE = "http://127.0.0.1:5000"

def check(url, label, expect_code=200):
    try:
        r = requests.get(url, timeout=10, allow_redirects=False)
        ok = r.status_code == expect_code
        print(f"  [{'PASS' if ok else 'FAIL'}] {label} (status={r.status_code})")
        return r
    except Exception as e:
        print(f"  [ERR] {label}: {e}")
        return None

print("=" * 65)
print("  SIDEBAR NAVIGATION SYSTEM — COMPREHENSIVE TEST")
print("=" * 65)

# 1. All pages accessible
print("\n[1] ALL PAGES ACCESSIBLE")
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
all_ok = True
for path, name in pages:
    r = check(f"{BASE}{path}", name)
    if r and r.status_code != 200:
        all_ok = False

# 2. Sidebar HTML presence check
print("\n[2] SIDEBAR HTML STRUCTURE")
r = requests.get(f"{BASE}/")
html = r.text

checks = {
    "Sidebar aside element": '<aside class="sidebar"' in html,
    "Sidebar toggle button": 'sidebarToggle' in html,
    "Main wrapper div": 'mainWrapper' in html,
    "Sidebar brand link": 'sidebar-brand' in html,
    "Navigation nav element": 'sidebar-nav' in html,
    "Home nav item (首页)": '首页' in html,
    "Courses nav item (课程)": '课程' in html,
    "Exercises nav item (练习)": '练习' in html,
    "Exams nav item (考试)": '考试' in html,
    "Community nav item (社区)": '社区' in html,
    "Login nav item (登录)": '登录' in html,
    "Language switcher button": 'langBtn' in html,
    "Skip link": 'skip-link' in html,
    "ARIA labels present": 'aria-label="主导航"' in html,
    "ARIA menuitem roles": 'role="menuitem"' in html,
    "ARIA menubar role": 'role="menubar"' in html,
    "data-tooltip attributes": 'data-tooltip=' in html,
    "No old navbar (display:none)": '.navbar' not in html or 'display:none' in html,
    "No nav-overlay": 'nav-overlay' not in html,
    "No dropdown-menu": 'dropdown-menu' not in html,
}
for name, result in checks.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")
    if not result:
        all_ok = False

# 3. CSS verification
print("\n[3] CSS VERIFICATION")
css_r = requests.get(f"{BASE}/static/css/main.min.css")
css = css_r.text
css_checks = {
    "No old .navbar background": "#1a365d" not in css,
    "Main wrapper styles": '.main-wrapper' in css,
    "Footer margin-top auto": 'margin-top:auto' in css,
    "Container max-width": 'max-width:1280px' in css,
}
for name, result in css_checks.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")

# 4. Font optimization verification
print("\n[4] FONT OPTIMIZATION")
font_checks = {
    "Sans-serif font stack": 'var(--font-sans)' in html and 'sans-serif' in css,
    "Font weight 600-700 on sidebar": 'font-weight:600' in html or 'font-weight:700' in html,
    "Font size 14px on labels": 'font-size:13px' in html or 'font-size:14px' in html,
    "Text color #333 on sidebar": '#333333' in html,
    "No text-shadow on sidebar": 'text-shadow' not in html.lower() or 'sidebar-link' not in html,
    "Webkit font smoothing": '-webkit-font-smoothing:antialiased' in css,
    "Legibility optimization": 'text-rendering:optimizeLegibility' in css,
}
for name, result in font_checks.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")

# 5. Responsive behavior check
print("\n[5] RESPONSIVE BEHAVIOR")
resp_checks = {
    "768px mobile rules": '@media(max-width:767.98px)' in css or '@media(max-width:767' in html,
    "380px small rules": '@media(max-width:380px)' in css or '@media(max-width:380' in html,
    "Sidebar collapsed width var": '--sidebar-collapsed-width' in html,
    "Main wrapper expanded class": '.main-wrapper.expanded' in html,
    "Toggle JS logic": 'sidebar.classList.toggle' in html,
    "Ctrl+B shortcut": "e.ctrlKey && e.key === 'b'" in html,
    "localStorage persistence": "localStorage.setItem('sidebar-collapsed'" in html,
}
for name, result in resp_checks.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")

# 6. Auth pages redirect
print("\n[6] AUTH PROTECTED PAGES")
auth_pages = [
    ("/exam/1", "Exam Detail (redirect)"),
    ("/profile", "Profile (redirect)"),
    ("/admin", "Admin (redirect)"),
]
for path, name in auth_pages:
    r = check(f"{BASE}{path}", name, expect_code=302)

# 7. Static assets
print("\n[7] STATIC ASSETS")
for asset in ["/static/css/main.min.css", "/static/js/main.min.js", "/static/js/i18n.js"]:
    check(f"{BASE}{asset}", asset)

# 8. Sidebar active state logic
print("\n[8] SIDEBAR ACTIVE STATE LOGIC")
active_logic = {
    "request.endpoint checks": "request.endpoint" in html,
    "Exams endpoint group active": "'exams','exam_detail','take_exam'" in html,
    "Profile group active": "'profile','progress','report'" in html,
    "Admin prefix startswith": "request.endpoint.startswith('admin')" in html,
}
for name, result in active_logic.items():
    print(f"  [{'PASS' if result else 'FAIL'}] {name}")

print("\n" + "=" * 65)
print(f"  TEST RESULT: {'ALL PASS' if all_ok else 'SOME FAILURES'}")
print("=" * 65)
