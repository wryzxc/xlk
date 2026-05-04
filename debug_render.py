import sys
sys.path.insert(0, r'e:\安装包\28\python-learning-platform')

from app import app, Exercise

with app.app_context():
    with app.test_client() as client:
        # 先登录
        client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        })
        
        # 获取练习页面
        r = client.get('/exercise/1')
        print(f'Status: {r.status_code}')
        print(f'Content length: {len(r.data)}')
        
        # 检查是否有错误信息
        text = r.data.decode('utf-8')
        if 'Traceback' in text:
            print('\n--- TEMPLATE ERROR ---')
            print(text[:2000])
        else:
            print('\n--- First 1000 chars ---')
            print(text[:1000])
            print('\n--- Last 1000 chars ---')
            print(text[-1000:])
            
        # 检查关键内容
        print(f'\nContains "CodeMirror": {"CodeMirror" in text}')
        print(f'Contains "codemirror": {"codemirror" in text.lower()}')
