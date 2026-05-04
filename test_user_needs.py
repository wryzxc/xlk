"""
User Needs Analysis Validation Test
Tests all implemented improvements against success metrics
"""
import requests

BASE = 'http://127.0.0.1:5000'
session = requests.Session()

print('=' * 70)
print('User Needs Analysis - Implementation Validation')
print('=' * 70)

# Login
r = session.post(f'{BASE}/login', data={'username': 'admin', 'password': 'admin123'}, timeout=10)
print(f'\n[1] Login: {r.status_code}')

# Test Profile Page Enhancements
r = session.get(f'{BASE}/profile', timeout=10)
text = r.text
print(f'[2] Profile Page: {r.status_code}')

# Check gamification elements
gamification = {
    'Achievement Badges': 'achievement-badge' in text,
    'Skill Progress Bars': 'skill-item' in text,
    'Learning Heatmap': 'heatmap-cell' in text,
    'Streak Counter': 'streakDays' in text or '连续学习' in text,
    'Activity Feed': 'activity-item' in text,
}
print('\n[3] Gamification Features:')
for feature, exists in gamification.items():
    print(f'    {feature}: {"OK" if exists else "FAIL"}')

# Test Admin Dashboard
r = session.get(f'{BASE}/admin', timeout=10)
text = r.text
print(f'\n[4] Admin Dashboard: {r.status_code}')

admin_features = {
    'Charts': 'canvas id=' in text,
    'User Table': 'userTable' in text,
    'Log System': 'logContainer' in text,
    'Filter Controls': 'filter-input' in text,
    'Statistics Cards': 'stat-card' in text,
}
print('\n[5] Admin Dashboard Features:')
for feature, exists in admin_features.items():
    print(f'    {feature}: {"OK" if exists else "FAIL"}')

# Test Exercise Editor Reset
r = session.get(f'{BASE}/exercise/1', timeout=10)
text = r.text
print(f'\n[6] Exercise Editor: {r.status_code}')

editor_features = {
    'Reset Button': 'resetCode()' in text,
    'Clear Button': 'clearCode()' in text,
    'CodeMirror Editor': 'CodeMirror' in text,
    'Run Button': 'runCode()' in text,
    'Submit Button': 'submitCode()' in text,
}
print('\n[7] Editor Features:')
for feature, exists in editor_features.items():
    print(f'    {feature}: {"OK" if exists else "FAIL"}')

# Test Mobile Responsiveness
responsive = {
    'Viewport Meta': 'viewport' in text,
    'Media Queries': '@media' in text,
    'Flexible Layout': 'grid' in text or 'flex' in text,
}
print('\n[8] Mobile Responsiveness:')
for feature, exists in responsive.items():
    print(f'    {feature}: {"OK" if exists else "FAIL"}')

print('\n' + '=' * 70)
print('Success Metrics Validation')
print('=' * 70)
print('\nMetric 1: Profile page shows all gamification elements')
print('  Target: 100% of elements present')
print('  Result:', f'{sum(gamification.values())}/{len(gamification)} elements')

print('\nMetric 2: Admin dashboard provides comprehensive analytics')
print('  Target: All 5 feature categories present')
print('  Result:', f'{sum(admin_features.values())}/{len(admin_features)} categories')

print('\nMetric 3: Code editor supports full reset functionality')
print('  Target: Reset and clear buttons both available')
print('  Result:', 'PASS' if editor_features['Reset Button'] and editor_features['Clear Button'] else 'FAIL')

print('\nMetric 4: Responsive design for mobile devices')
print('  Target: Viewport and media queries present')
print('  Result:', 'PASS' if all(responsive.values()) else 'FAIL')

print('\n' + '=' * 70)
print('Validation Complete!')
print('=' * 70)
