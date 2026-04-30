# -*- coding: utf-8 -*-
"""课程增强内容模块 - 为学习资源添加补充教育内容"""

# ============================================================
# 1. 课程级增强内容 - 学习目标、背景知识、学习路径
# ============================================================

COURSE_ENHANCEMENTS = {
    1: {  # Python基础入门
        "learning_objectives_detailed": [
            {"obj": "理解Python语言的设计哲学和核心特点", "level": "记忆", "skill": "概念理解"},
            {"obj": "熟练搭建Python开发环境并运行程序", "level": "应用", "skill": "环境配置"},
            {"obj": "掌握变量命名规范和数据类型转换", "level": "应用", "skill": "基础语法"},
            {"obj": "运用各种运算符解决实际计算问题", "level": "应用", "skill": "计算能力"},
            {"obj": "编写条件语句处理多分支逻辑", "level": "应用", "skill": "逻辑控制"},
            {"obj": "使用循环结构处理重复性任务", "level": "应用", "skill": "迭代思维"},
            {"obj": "定义和调用函数实现代码复用", "level": "应用", "skill": "函数编程"},
            {"obj": "使用模块组织代码并调用标准库", "level": "应用", "skill": "模块化"},
        ],
        "background_knowledge": {
            "title": "编程语言发展简史",
            "content": """<div class='bg-knowledge-section'>
<h4>从机器语言到高级语言</h4>
<p>计算机程序设计语言经历了从机器语言（0和1）到汇编语言，再到高级语言的演变过程。Python属于高级语言中的解释型语言。</p>
<h4>Python的诞生</h4>
<p>1989年圣诞节期间，Guido van Rossum在荷兰开始编写Python。1991年发布第一个版本。名字来源于他喜爱的喜剧团体Monty Python。</p>
<h4>Python的设计哲学</h4>
<blockquote class='philosophy-quote'>
    <p>"优美优于丑陋，显式优于隐式，简单优于复杂，复杂优于凌乱。"</p>
    <cite>—— The Zen of Python</cite>
</blockquote>
<p>在Python解释器中输入 <code>import this</code> 即可查看完整的Python之禅。</p>
</div>"""
        },
        "learning_path_guide": {
            "title": "学习路径指引",
            "steps": [
                {"step": 1, "title": "环境准备", "desc": "安装Python和代码编辑器，运行第一个程序", "time": "15分钟"},
                {"step": 2, "title": "概念理解", "desc": "理解变量、数据类型、运算符的基本概念", "time": "40分钟"},
                {"step": 3, "title": "逻辑控制", "desc": "掌握条件判断和循环结构", "time": "45分钟"},
                {"step": 4, "title": "函数基础", "desc": "学习函数定义、参数传递和返回值", "time": "50分钟"},
                {"step": 5, "title": "模块应用", "desc": "使用标准库和自定义模块", "time": "30分钟"},
                {"step": 6, "title": "综合实践", "desc": "完成学生成绩管理系统项目", "time": "60分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "mindmap",
                "title": "Python基础知识体系",
                "data": {
                    "核心": ["变量与数据类型", "运算符", "控制流", "函数", "模块"],
                    "变量与数据类型": ["int", "float", "str", "bool", "类型转换"],
                    "运算符": ["算术", "比较", "逻辑", "赋值", "成员", "身份"],
                    "控制流": ["if-elif-else", "for循环", "while循环", "break/continue"],
                    "函数": ["定义", "参数", "返回值", "lambda", "作用域"],
                    "模块": ["import", "标准库", "自定义", "包"]
                }
            }
        ],
        "extended_reading": [
            {"title": "Python官方文档", "url": "https://docs.python.org/zh-cn/3/", "desc": "最权威的学习参考资料"},
            {"title": "Python之禅详解", "url": "https://peps.python.org/pep-0020/", "desc": "深入理解Python设计哲学"},
            {"title": "廖雪峰Python教程", "url": "https://www.liaoxuefeng.com/wiki/1016959663602400", "desc": "中文优质入门教程"},
        ],
        "case_studies": [
            {
                "title": "案例：温度转换器",
                "scenario": "某气象站需要将摄氏温度数据批量转换为华氏温度",
                "analysis": "使用函数封装转换逻辑，利用循环处理批量数据",
                "solution": """def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

temperatures = [0, 10, 20, 30, 40]
for t in temperatures:
    print(f"{t}°C = {celsius_to_fahrenheit(t):.1f}°F")""",
                "key_takeaway": "函数+循环是解决批量数据处理的标准模式"
            }
        ]
    },
    2: {  # Python数据结构
        "learning_objectives_detailed": [
            {"obj": "理解不同数据结构的特点和适用场景", "level": "理解", "skill": "数据结构选型"},
            {"obj": "熟练进行列表的增删改查和切片操作", "level": "应用", "skill": "列表操作"},
            {"obj": "掌握元组的不可变性和解包技巧", "level": "应用", "skill": "元组应用"},
            {"obj": "使用字典进行高效的键值对数据管理", "level": "应用", "skill": "字典操作"},
            {"obj": "运用集合进行去重和集合运算", "level": "应用", "skill": "集合应用"},
            {"obj": "理解深浅拷贝的区别和应用场景", "level": "理解", "skill": "内存管理"},
        ],
        "background_knowledge": {
            "title": "数据结构的重要性",
            "content": """<div class='bg-knowledge-section'>
<h4>为什么数据结构很重要？</h4>
<p>数据结构是程序的骨架。选择合适的数据结构可以让代码更简洁、运行更高效。</p>
<h4>时间复杂度概念</h4>
<ul>
<li><strong>O(1)</strong> - 常数时间：字典查找、集合查找</li>
<li><strong>O(n)</strong> - 线性时间：列表遍历</li>
<li><strong>O(n²)</strong> - 平方时间：嵌套循环</li>
</ul>
<h4>Python内置数据结构性能对比</h4>
<table class='comparison-table'>
<tr><th>操作</th><th>列表</th><th>字典</th><th>集合</th></tr>
<tr><td>查找</td><td>O(n)</td><td>O(1)</td><td>O(1)</td></tr>
<tr><td>添加</td><td>O(1)</td><td>O(1)</td><td>O(1)</td></tr>
<tr><td>删除</td><td>O(n)</td><td>O(1)</td><td>O(1)</td></tr>
</table>
</div>"""
        },
        "learning_path_guide": {
            "title": "数据结构学习路径",
            "steps": [
                {"step": 1, "title": "列表精通", "desc": "掌握列表的所有操作和推导式", "time": "50分钟"},
                {"step": 2, "title": "元组与字符串", "desc": "理解不可变类型的特点", "time": "40分钟"},
                {"step": 3, "title": "字典应用", "desc": "学习字典的高级用法", "time": "45分钟"},
                {"step": 4, "title": "集合运算", "desc": "掌握集合的去重和运算", "time": "35分钟"},
                {"step": 5, "title": "综合应用", "desc": "使用数据结构解决实际问题", "time": "40分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "comparison",
                "title": "数据结构特性对比",
                "data": [
                    {"结构": "列表", "有序": "是", "可变": "是", "重复": "允许", "查找": "O(n)"},
                    {"结构": "元组", "有序": "是", "可变": "否", "重复": "允许", "查找": "O(n)"},
                    {"结构": "字典", "有序": "是*", "可变": "是", "重复": "键不重复", "查找": "O(1)"},
                    {"结构": "集合", "无序": "是", "可变": "是", "重复": "不重复", "查找": "O(1)"},
                ]
            }
        ],
        "extended_reading": [
            {"title": "Python数据结构文档", "url": "https://docs.python.org/zh-cn/3/tutorial/datastructures.html", "desc": "官方数据结构教程"},
            {"title": "算法与数据结构可视化", "url": "https://visualgo.net/zh", "desc": "直观理解数据结构运作原理"},
        ],
        "case_studies": [
            {
                "title": "案例：购物车系统",
                "scenario": "电商网站需要实现购物车功能，支持添加商品、修改数量、计算总价",
                "analysis": "使用字典存储商品和数量，利用集合处理优惠券的去重",
                "solution": """cart = {}
def add_to_cart(item, qty=1):
    cart[item] = cart.get(item, 0) + qty

def get_total(prices):
    return sum(prices[item] * qty for item, qty in cart.items())""",
                "key_takeaway": "字典适合存储键值对关系，推导式简化数据处理"
            }
        ]
    },
    3: {  # 面向对象编程
        "learning_objectives_detailed": [
            {"obj": "理解类与对象的概念及关系", "level": "理解", "skill": "OOP思维"},
            {"obj": "掌握封装、继承、多态三大特性", "level": "应用", "skill": "OOP设计"},
            {"obj": "使用魔术方法增强类的功能", "level": "应用", "skill": "高级OOP"},
            {"obj": "应用设计原则编写可维护代码", "level": "应用", "skill": "软件设计"},
        ],
        "background_knowledge": {
            "title": "面向对象编程思想",
            "content": """<div class='bg-knowledge-section'>
<h4>从过程式到面向对象</h4>
<p>过程式编程关注"怎么做"（步骤），面向对象编程关注"谁来做"（对象）。</p>
<h4>现实世界的映射</h4>
<p>类是模板（如"汽车图纸"），对象是实例（如"一辆具体的汽车"）。</p>
<h4>四大特性</h4>
<ul>
<li><strong>抽象</strong>：提取共同特征，忽略细节</li>
<li><strong>封装</strong>：隐藏内部实现，暴露接口</li>
<li><strong>继承</strong>：复用已有代码，扩展功能</li>
<li><strong>多态</strong>：同一接口，不同实现</li>
</ul>
</div>"""
        },
        "learning_path_guide": {
            "title": "OOP学习路径",
            "steps": [
                {"step": 1, "title": "类与对象", "desc": "理解基本概念，创建简单类", "time": "45分钟"},
                {"step": 2, "title": "封装", "desc": "学习访问控制和属性保护", "time": "35分钟"},
                {"step": 3, "title": "继承", "desc": "掌握继承和方法重写", "time": "45分钟"},
                {"step": 4, "title": "多态", "desc": "理解动态绑定的威力", "time": "30分钟"},
                {"step": 5, "title": "魔术方法", "desc": "使用魔术方法增强类", "time": "40分钟"},
                {"step": 6, "title": "设计原则", "desc": "学习SOLID原则", "time": "35分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "diagram",
                "title": "类继承关系图",
                "svg": """<svg viewBox='0 0 400 300' class='oop-diagram'>
<rect x='150' y='20' width='100' height='40' fill='#4f46e5' rx='5'/>
<text x='200' y='45' text-anchor='middle' fill='white' font-size='14'>Animal</text>
<line x1='200' y1='60' x2='100' y2='100' stroke='#666' stroke-width='2'/>
<line x1='200' y1='60' x2='300' y2='100' stroke='#666' stroke-width='2'/>
<rect x='50' y='100' width='100' height='40' fill='#059669' rx='5'/>
<text x='100' y='125' text-anchor='middle' fill='white' font-size='14'>Dog</text>
<rect x='250' y='100' width='100' height='40' fill='#059669' rx='5'/>
<text x='300' y='125' text-anchor='middle' fill='white' font-size='14'>Cat</text>
<line x1='100' y1='140' x2='100' y2='180' stroke='#666' stroke-width='2'/>
<line x1='300' y1='140' x2='300' y2='180' stroke='#666' stroke-width='2'/>
<rect x='50' y='180' width='100' height='40' fill='#d97706' rx='5'/>
<text x='100' y='205' text-anchor='middle' fill='white' font-size='14'>Golden</text>
<rect x='250' y='180' width='100' height='40' fill='#d97706' rx='5'/>
<text x='300' y='205' text-anchor='middle' fill='white' font-size='14'>Persian</text>
</svg>"""
            }
        ],
        "extended_reading": [
            {"title": "Python OOP教程", "url": "https://docs.python.org/zh-cn/3/tutorial/classes.html", "desc": "官方面向对象编程教程"},
            {"title": "设计模式", "url": "https://refactoringguru.cn/design-patterns/python", "desc": "Python设计模式详解"},
        ],
        "case_studies": [
            {
                "title": "案例：图形绘制系统",
                "scenario": "设计一个图形绘制系统，支持圆形、矩形、三角形，能计算面积和周长",
                "analysis": "使用抽象基类定义Shape接口，各具体图形继承实现",
                "solution": """from abc import ABC, abstractmethod
import math

class Shape(ABC):
    @abstractmethod
    def area(self): pass
    
    @abstractmethod
    def perimeter(self): pass

class Circle(Shape):
    def __init__(self, r): self.r = r
    def area(self): return math.pi * self.r ** 2
    def perimeter(self): return 2 * math.pi * self.r""",
                "key_takeaway": "抽象基类+继承是多态的基础"
            }
        ]
    },
    4: {  # 文件操作与异常处理
        "learning_objectives_detailed": [
            {"obj": "掌握文件的读写操作和上下文管理", "level": "应用", "skill": "文件IO"},
            {"obj": "理解异常处理机制并编写健壮代码", "level": "应用", "skill": "异常处理"},
            {"obj": "使用JSON和CSV进行数据序列化", "level": "应用", "skill": "数据交换"},
            {"obj": "设计自定义异常类", "level": "应用", "skill": "错误设计"},
        ],
        "background_knowledge": {
            "title": "文件系统与数据持久化",
            "content": """<div class='bg-knowledge-section'>
<h4>计算机存储层次</h4>
<p>寄存器 → 缓存 → 内存 → 硬盘 → 网络存储。文件操作涉及内存与硬盘的交互。</p>
<h4>编码与字符集</h4>
<ul>
<li><strong>ASCII</strong>：128个字符，1字节</li>
<li><strong>UTF-8</strong>：变长编码，兼容ASCII，中文3字节</li>
<li><strong>GBK</strong>：中文2字节</li>
</ul>
<p>Python 3默认使用UTF-8编码，处理中文文件时建议显式指定encoding='utf-8'。</p>
</div>"""
        },
        "learning_path_guide": {
            "title": "文件操作学习路径",
            "steps": [
                {"step": 1, "title": "文件基础", "desc": "学习打开、读取、写入文件", "time": "40分钟"},
                {"step": 2, "title": "异常处理", "desc": "掌握try-except结构", "time": "45分钟"},
                {"step": 3, "title": "JSON处理", "desc": "序列化和反序列化数据", "time": "35分钟"},
                {"step": 4, "title": "CSV处理", "desc": "表格数据的读写", "time": "35分钟"},
                {"step": 5, "title": "综合项目", "desc": "开发数据备份工具", "time": "50分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "flowchart",
                "title": "异常处理流程",
                "svg": """<svg viewBox='0 0 500 200' class='flowchart-diagram'>
<rect x='180' y='10' width='140' height='35' fill='#4f46e5' rx='5'/>
<text x='250' y='32' text-anchor='middle' fill='white' font-size='13'>try块执行代码</text>
<line x1='250' y1='45' x2='250' y2='70' stroke='#666' stroke-width='2'/>
<rect x='50' y='80' width='140' height='35' fill='#059669' rx='5'/>
<text x='120' y='102' text-anchor='middle' fill='white' font-size='13'>except捕获异常</text>
<rect x='310' y='80' width='140' height='35' fill='#059669' rx='5'/>
<text x='380' y='102' text-anchor='middle' fill='white' font-size='13'>else正常执行</text>
<line x1='250' y1='70' x2='120' y2='80' stroke='#666' stroke-width='2'/>
<line x1='250' y1='70' x2='380' y2='80' stroke='#666' stroke-width='2'/>
<line x1='120' y1='115' x2='250' y2='150' stroke='#666' stroke-width='2'/>
<line x1='380' y1='115' x2='250' y2='150' stroke='#666' stroke-width='2'/>
<rect x='180' y='150' width='140' height='35' fill='#7c3aed' rx='5'/>
<text x='250' y='172' text-anchor='middle' fill='white' font-size='13'>finally清理资源</text>
</svg>"""
            }
        ],
        "extended_reading": [
            {"title": "Python文件IO", "url": "https://docs.python.org/zh-cn/3/tutorial/inputoutput.html", "desc": "官方文件操作教程"},
            {"title": "异常处理最佳实践", "url": "https://docs.python.org/zh-cn/3/tutorial/errors.html", "desc": "官方异常处理指南"},
        ],
        "case_studies": [
            {
                "title": "案例：配置文件管理器",
                "scenario": "应用需要读取JSON配置文件，处理文件不存在或格式错误的情况",
                "analysis": "使用try-except处理各种异常，提供默认值",
                "solution": """import json
import os

def load_config(path='config.json'):
    defaults = {'debug': False, 'port': 8080}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
            defaults.update(config)
    except FileNotFoundError:
        print(f'配置文件不存在，使用默认配置')
    except json.JSONDecodeError:
        print(f'配置文件格式错误')
    return defaults""",
                "key_takeaway": "异常处理让程序更健壮，默认值保证可用性"
            }
        ]
    },
    5: {  # Python高级特性
        "learning_objectives_detailed": [
            {"obj": "理解迭代器协议和生成器原理", "level": "理解", "skill": "迭代思维"},
            {"obj": "使用装饰器扩展函数功能", "level": "应用", "skill": "元编程"},
            {"obj": "掌握函数式编程技巧", "level": "应用", "skill": "函数式编程"},
            {"obj": "使用正则表达式处理文本", "level": "应用", "skill": "文本处理"},
            {"obj": "理解上下文管理器的实现机制", "level": "理解", "skill": "资源管理"},
        ],
        "background_knowledge": {
            "title": "Python高级特性概览",
            "content": """<div class='bg-knowledge-section'>
<h4>迭代器 vs 生成器</h4>
<p>迭代器是<strong>一次性</strong>的，生成器是<strong>惰性</strong>的。生成器用yield暂停执行，节省内存。</p>
<h4>装饰器本质</h4>
<p>装饰器是一个返回函数的高阶函数。@语法糖让代码更优雅。</p>
<h4>函数式编程</h4>
<p>Python支持部分函数式编程特性：lambda、map、filter、reduce。函数是一等公民。</p>
</div>"""
        },
        "learning_path_guide": {
            "title": "高级特性学习路径",
            "steps": [
                {"step": 1, "title": "迭代器与生成器", "desc": "理解惰性求值和内存优化", "time": "45分钟"},
                {"step": 2, "title": "装饰器", "desc": "掌握装饰器的编写和应用", "time": "50分钟"},
                {"step": 3, "title": "高阶函数", "desc": "学习函数式编程技巧", "time": "40分钟"},
                {"step": 4, "title": "上下文管理器", "desc": "实现自定义上下文管理器", "time": "35分钟"},
                {"step": 5, "title": "正则表达式", "desc": "掌握文本模式匹配", "time": "40分钟"},
                {"step": 6, "title": "综合项目", "desc": "开发日志分析工具", "time": "50分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "comparison",
                "title": "列表 vs 生成器内存占用",
                "data": [
                    {"方式": "列表", "内存": "O(n)", "创建": "立即", "复用": "可多次"},
                    {"方式": "生成器", "内存": "O(1)", "创建": "惰性", "复用": "一次性"},
                ]
            }
        ],
        "extended_reading": [
            {"title": "Python生成器详解", "url": "https://docs.python.org/zh-cn/3/tutorial/classes.html#generators", "desc": "官方生成器教程"},
            {"title": "正则表达式教程", "url": "https://docs.python.org/zh-cn/3/library/re.html", "desc": "官方正则表达式文档"},
        ],
        "case_studies": [
            {
                "title": "案例：大数据文件处理",
                "scenario": "需要处理10GB的日志文件，统计错误数量，内存只有8GB",
                "analysis": "使用生成器逐行读取，避免一次性加载整个文件",
                "solution": """def read_large_file(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip()

def count_errors(filepath):
    return sum(1 for line in read_large_file(filepath) if 'ERROR' in line)""",
                "key_takeaway": "生成器是处理大数据的利器，内存占用恒定"
            }
        ]
    },
    6: {  # Web开发基础
        "learning_objectives_detailed": [
            {"obj": "理解Web应用架构和HTTP协议", "level": "理解", "skill": "Web基础"},
            {"obj": "使用Flask创建路由和处理请求", "level": "应用", "skill": "后端开发"},
            {"obj": "使用Jinja2模板渲染动态页面", "level": "应用", "skill": "模板引擎"},
            {"obj": "实现表单处理和用户认证", "level": "应用", "skill": "用户系统"},
            {"obj": "使用SQLAlchemy进行数据库操作", "level": "应用", "skill": "ORM"},
            {"obj": "设计RESTful API接口", "level": "应用", "skill": "API设计"},
        ],
        "background_knowledge": {
            "title": "Web开发基础概念",
            "content": """<div class='bg-knowledge-section'>
<h4>HTTP协议基础</h4>
<ul>
<li><strong>GET</strong>：获取资源，参数在URL中</li>
<li><strong>POST</strong>：提交数据，参数在请求体中</li>
<li><strong>PUT</strong>：更新资源</li>
<li><strong>DELETE</strong>：删除资源</li>
</ul>
<h4>MVC架构</h4>
<p>Model（数据模型）- View（视图模板）- Controller（控制器/路由）</p>
<h4>前后端分离</h4>
<p>前端负责界面渲染，后端提供API接口，通过JSON交换数据。</p>
</div>"""
        },
        "learning_path_guide": {
            "title": "Web开发学习路径",
            "steps": [
                {"step": 1, "title": "Flask基础", "desc": "创建应用，定义路由", "time": "50分钟"},
                {"step": 2, "title": "模板渲染", "desc": "使用Jinja2渲染页面", "time": "45分钟"},
                {"step": 3, "title": "表单处理", "desc": "处理用户输入和文件上传", "time": "45分钟"},
                {"step": 4, "title": "数据库集成", "desc": "使用SQLAlchemy操作数据库", "time": "50分钟"},
                {"step": 5, "title": "RESTful API", "desc": "设计API接口", "time": "40分钟"},
                {"step": 6, "title": "综合项目", "desc": "开发Todo List应用", "time": "60分钟"},
            ]
        },
        "visual_charts": [
            {
                "type": "diagram",
                "title": "Web应用架构图",
                "svg": """<svg viewBox='0 0 500 280' class='web-arch-diagram'>
<rect x='180' y='10' width='140' height='40' fill='#4f46e5' rx='5'/>
<text x='250' y='35' text-anchor='middle' fill='white' font-size='14'>浏览器/客户端</text>
<line x1='250' y1='50' x2='250' y2='80' stroke='#666' stroke-width='2' marker-end='url(#arrow)'/>
<rect x='150' y='85' width='200' height='40' fill='#059669' rx='5'/>
<text x='250' y='110' text-anchor='middle' fill='white' font-size='14'>Flask应用服务器</text>
<line x1='200' y1='125' x2='120' y2='160' stroke='#666' stroke-width='2'/>
<line x1='300' y1='125' x2='380' y2='160' stroke='#666' stroke-width='2'/>
<rect x='50' y='165' width='140' height='40' fill='#d97706' rx='5'/>
<text x='120' y='190' text-anchor='middle' fill='white' font-size='13'>Jinja2模板</text>
<rect x='310' y='165' width='140' height='40' fill='#d97706' rx='5'/>
<text x='380' y='190' text-anchor='middle' fill='white' font-size='13'>SQLAlchemy/数据库</text>
<line x1='250' y1='125' x2='250' y2='200' stroke='#666' stroke-width='2'/>
<rect x='180' y='205' width='140' height='40' fill='#7c3aed' rx='5'/>
<text x='250' y='230' text-anchor='middle' fill='white' font-size='13'>路由/视图函数</text>
<defs><marker id='arrow' markerWidth='10' markerHeight='10' refX='9' refY='3' orient='auto'><path d='M0,0 L0,6 L9,3 z' fill='#666'/></marker></defs>
</svg>"""
            }
        ],
        "extended_reading": [
            {"title": "Flask官方文档", "url": "https://flask.palletsprojects.com/", "desc": "Flask框架官方文档"},
            {"title": "HTTP协议详解", "url": "https://developer.mozilla.org/zh-CN/docs/Web/HTTP", "desc": "MDN HTTP教程"},
            {"title": "RESTful API设计", "url": "https://restfulapi.net/", "desc": "RESTful API最佳实践"},
        ],
        "case_studies": [
            {
                "title": "案例：用户认证系统",
                "scenario": "实现用户注册、登录、登出功能，使用session保持登录状态",
                "analysis": "使用Flask session存储用户ID，密码使用哈希存储",
                "solution": """from flask import Flask, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash

@app.route('/login', methods=['POST'])
def login():
    user = User.query.filter_by(username=request.form['username']).first()
    if user and check_password_hash(user.password_hash, request.form['password']):
        session['user_id'] = user.id
        return redirect('/dashboard')
    return '登录失败', 401""",
                "key_takeaway": "安全存储密码，使用session管理状态"
            }
        ]
    }
}


# ============================================================
# 2. 课时级增强内容 - 重点注释、交互式练习、知识检测
# ============================================================

LESSON_ENHANCEMENTS = {
    # Course 1 Lessons
    1: {  # Python简介与环境搭建
        "key_annotations": [
            {"term": "解释型语言", "desc": "代码逐行执行，无需预先编译成机器码，开发效率高但运行速度相对较慢"},
            {"term": "动态类型", "desc": "变量类型在运行时确定，无需显式声明，灵活但可能隐藏类型错误"},
            {"term": "REPL", "desc": "Read-Eval-Print Loop，交互式解释器，适合快速测试代码片段"},
        ],
        "interactive_checkpoints": [
            {"question": "Python是编译型语言还是解释型语言？", "answer": "解释型", "type": "choice", "options": ["编译型", "解释型", "两者都是"]},
            {"question": "在终端输入什么命令可以查看Python版本？", "answer": "python --version", "type": "fill"},
        ],
        "common_pitfalls": [
            {"pitfall": "安装时未勾选'Add Python to PATH'", "solution": "重新安装或手动添加环境变量"},
            {"pitfall": "文件名使用了Python关键字如test.py", "solution": "避免使用test、code等可能与标准库冲突的名字"},
        ]
    },
    2: {  # 变量与数据类型
        "key_annotations": [
            {"term": "变量", "desc": "内存中存储数据的命名位置，Python中变量是对象的引用"},
            {"term": "垃圾回收", "desc": "Python自动管理内存，当对象不再被引用时自动释放"},
            {"term": "is vs ==", "desc": "is比较身份（内存地址），==比较值。小整数和短字符串会被缓存"},
        ],
        "interactive_checkpoints": [
            {"question": "表达式 type(3.0) 的结果是什么？", "answer": "float", "type": "choice", "options": ["int", "float", "str", "double"]},
            {"question": "以下哪个变量名是合法的？", "answer": "_name", "type": "choice", "options": ["2name", "my-name", "_name", "class"]},
        ],
        "common_pitfalls": [
            {"pitfall": "浮点数精度问题：0.1 + 0.2 != 0.3", "solution": "使用decimal模块或round()函数处理精度"},
            {"pitfall": "字符串和数字拼接报错", "solution": "使用str()转换或使用f-string"},
        ]
    },
    3: {  # 运算符
        "key_annotations": [
            {"term": "短路求值", "desc": "and和or运算符在能确定结果时不再计算后续表达式"},
            {"term": "运算符优先级", "desc": "幂运算 > 正负号 > 乘除 > 加减 > 比较 > 逻辑"},
            {"term": "海象运算符:=", "desc": "Python 3.8+，在表达式中赋值，如 while (n:=len(x)) > 0"},
        ],
        "interactive_checkpoints": [
            {"question": "表达式 10 // 3 的结果是？", "answer": "3", "type": "choice", "options": ["3", "3.33", "1", "3.0"]},
            {"question": "True and False or True 的结果是？", "answer": "True", "type": "choice", "options": ["True", "False", "None", "报错"]},
        ],
        "common_pitfalls": [
            {"pitfall": "使用=代替==进行比较", "solution": "比较用==，赋值用="},
            {"pitfall": "is用于比较值", "solution": "比较值用==，is用于判断是否是同一对象"},
        ]
    },
    4: {  # 条件语句
        "key_annotations": [
            {"term": "真值测试", "desc": "0、空序列、None被视为False，其他为True"},
            {"term": "三元表达式", "desc": "x if condition else y，Python中唯一的三目运算符形式"},
            {"term": "链式比较", "desc": "1 < x < 10 等价于 1 < x and x < 10，更简洁"},
        ],
        "interactive_checkpoints": [
            {"question": "以下哪个值在if判断中为False？", "answer": "[]", "type": "choice", "options": ["1", "[0]", "[]", "'False'"]},
            {"question": "将 '成年' if age >= 18 else '未成年' 改写为普通if语句", "answer": "if age >= 18: result = '成年' else: result = '未成年'", "type": "fill"},
        ],
        "common_pitfalls": [
            {"pitfall": "忘记冒号", "solution": "if/for/while/def/class语句末尾必须有冒号"},
            {"pitfall": "缩进不一致", "solution": "统一使用4个空格缩进，不要用Tab"},
        ]
    },
    5: {  # 循环结构
        "key_annotations": [
            {"term": "可迭代对象", "desc": "实现了__iter__方法的对象，如列表、字符串、字典、文件"},
            {"term": "range对象", "desc": "惰性生成的数字序列，节省内存。range(1000000)不占大量内存"},
            {"term": "enumerate", "desc": "同时获取索引和值，避免手动维护计数器变量"},
        ],
        "interactive_checkpoints": [
            {"question": "range(5)生成的序列是？", "answer": "0,1,2,3,4", "type": "choice", "options": ["1,2,3,4,5", "0,1,2,3,4", "0,1,2,3,4,5", "1,2,3,4"]},
            {"question": "在循环中用什么语句提前结束整个循环？", "answer": "break", "type": "fill"},
        ],
        "common_pitfalls": [
            {"pitfall": "在for循环中修改正在遍历的列表", "solution": "遍历副本：for x in list[:]"},
            {"pitfall": "while循环忘记更新条件变量导致死循环", "solution": "确保循环条件最终会变为False"},
        ]
    },
    6: {  # 函数基础
        "key_annotations": [
            {"term": "LEGB规则", "desc": "变量查找顺序：Local → Enclosing → Global → Built-in"},
            {"term": "一等公民", "desc": "函数在Python中是一等对象，可以赋值给变量、作为参数、作为返回值"},
            {"term": "闭包", "desc": "函数记住并访问其词法作用域，即使函数在当前作用域外执行"},
        ],
        "interactive_checkpoints": [
            {"question": "def func(a, b=2, *args) 中，b是什么类型的参数？", "answer": "默认参数", "type": "choice", "options": ["位置参数", "默认参数", "可变参数", "关键字参数"]},
            {"question": "函数中修改全局变量需要使用什么关键字声明？", "answer": "global", "type": "fill"},
        ],
        "common_pitfalls": [
            {"pitfall": "使用可变对象作为默认参数", "solution": "使用None作为默认值，函数内初始化"},
            {"pitfall": "忘记return返回值", "solution": "没有return的函数返回None"},
        ]
    },
    7: {  # 模块与包
        "key_annotations": [
            {"term": "命名空间", "desc": "变量名到对象的映射，模块有自己的命名空间避免命名冲突"},
            {"term": "__name__", "desc": "模块被直接运行时值为'__main__'，被导入时为模块名"},
            {"term": "包", "desc": "包含__init__.py的目录，可以组织多个模块"},
        ],
        "interactive_checkpoints": [
            {"question": "从math模块导入sqrt函数的正确语法是？", "answer": "from math import sqrt", "type": "choice", "options": ["import math.sqrt", "from math import sqrt", "include math.sqrt", "using math.sqrt"]},
            {"question": "模块被直接运行时，__name__的值是什么？", "answer": "__main__", "type": "fill"},
        ],
        "common_pitfalls": [
            {"pitfall": "循环导入", "solution": "重构代码，将公共部分提取到第三个模块"},
            {"pitfall": "模块名与标准库冲突", "solution": "避免使用code、test、random等作为文件名"},
        ]
    },
    8: {  # 综合项目
        "key_annotations": [
            {"term": "数据封装", "desc": "将数据和操作数据的方法组织在一起，是OOP的基础思想"},
            {"term": "字典嵌套", "desc": "字典的值可以是另一个字典，适合表示复杂数据结构"},
        ],
        "interactive_checkpoints": [
            {"question": "以下哪种数据结构最适合存储学生姓名到成绩的映射？", "answer": "字典", "type": "choice", "options": ["列表", "元组", "字典", "集合"]},
        ],
        "common_pitfalls": [
            {"pitfall": "直接修改遍历中的字典", "solution": "先获取所有键再修改，或创建新字典"},
        ]
    },
}


# ============================================================
# 3. 练习增强内容 - 解题思路、相关知识点、扩展挑战
# ============================================================

EXERCISE_ENHANCEMENTS = {
    "general": {
        "problem_solving_framework": """
<h4>解题思维框架</h4>
<ol class='problem-solving-steps'>
    <li><strong>理解题意</strong>：仔细阅读题目，明确输入和输出</li>
    <li><strong>分析示例</strong>：通过示例理解预期行为</li>
    <li><strong>设计算法</strong>：思考解决步骤，选择合适的数据结构</li>
    <li><strong>编写代码</strong>：将思路转化为Python代码</li>
    <li><strong>测试验证</strong>：用多种输入测试，包括边界情况</li>
    <li><strong>优化反思</strong>：思考是否有更优解法</li>
</ol>
""",
        "difficulty_guide": {
            "easy": "基础概念题，直接应用所学知识即可解决",
            "medium": "需要组合多个知识点，或进行简单逻辑推理",
            "hard": "需要深入理解原理，设计较复杂的算法"
        }
    }
}


# ============================================================
# 4. 通用学习工具 - 速查表、快捷键、常见错误
# ============================================================

LEARNING_TOOLS = {
    "python_cheatsheet": {
        "title": "Python速查表",
        "sections": [
            {
                "title": "数据类型",
                "items": [
                    {"code": "int(x)", "desc": "转换为整数"},
                    {"code": "float(x)", "desc": "转换为浮点数"},
                    {"code": "str(x)", "desc": "转换为字符串"},
                    {"code": "list(x)", "desc": "转换为列表"},
                    {"code": "dict(x)", "desc": "转换为字典"},
                    {"code": "type(x)", "desc": "查看类型"},
                ]
            },
            {
                "title": "列表操作",
                "items": [
                    {"code": "lst.append(x)", "desc": "末尾添加"},
                    {"code": "lst.insert(i, x)", "desc": "位置i插入"},
                    {"code": "lst.remove(x)", "desc": "删除第一个x"},
                    {"code": "lst.pop([i])", "desc": "删除并返回"},
                    {"code": "lst.sort()", "desc": "原地排序"},
                    {"code": "lst.reverse()", "desc": "原地反转"},
                    {"code": "len(lst)", "desc": "长度"},
                    {"code": "sum(lst)", "desc": "求和"},
                ]
            },
            {
                "title": "字符串方法",
                "items": [
                    {"code": "s.upper()", "desc": "大写"},
                    {"code": "s.lower()", "desc": "小写"},
                    {"code": "s.strip()", "desc": "去空白"},
                    {"code": "s.split(d)", "desc": "分割"},
                    {"code": "s.join(lst)", "desc": "连接"},
                    {"code": "s.replace(a, b)", "desc": "替换"},
                    {"code": "s.startswith(p)", "desc": "前缀判断"},
                    {"code": "s.find(sub)", "desc": "查找位置"},
                ]
            },
            {
                "title": "字典操作",
                "items": [
                    {"code": "d[key]", "desc": "取值（可能报错）"},
                    {"code": "d.get(key, default)", "desc": "安全取值"},
                    {"code": "d.keys()", "desc": "所有键"},
                    {"code": "d.values()", "desc": "所有值"},
                    {"code": "d.items()", "desc": "键值对"},
                    {"code": "d.update(d2)", "desc": "合并字典"},
                    {"code": "key in d", "desc": "判断存在"},
                ]
            },
        ]
    },
    "common_errors": {
        "title": "常见错误速查",
        "errors": [
            {"error": "SyntaxError: invalid syntax", "cause": "语法错误，检查冒号、括号、引号", "fix": "检查行末是否有冒号，括号是否配对"},
            {"error": "IndentationError", "cause": "缩进错误", "fix": "统一使用4个空格缩进"},
            {"error": "NameError", "cause": "使用了未定义的变量", "fix": "检查变量名拼写，确保先定义后使用"},
            {"error": "TypeError", "cause": "类型不匹配", "fix": "检查操作数的类型，必要时转换"},
            {"error": "IndexError", "cause": "索引越界", "fix": "检查索引是否在有效范围内"},
            {"error": "KeyError", "cause": "字典中不存在该键", "fix": "使用.get()方法或先检查key in dict"},
            {"error": "ValueError", "cause": "值不合适", "fix": "检查输入值的格式和范围"},
            {"error": "ZeroDivisionError", "cause": "除以零", "fix": "添加除数非零判断"},
            {"error": "FileNotFoundError", "cause": "文件不存在", "fix": "检查文件路径是否正确"},
            {"error": "AttributeError", "cause": "对象没有该属性", "fix": "检查对象类型，确认方法/属性存在"},
        ]
    }
}


def get_course_enhancement(course_id):
    """获取课程增强内容"""
    return COURSE_ENHANCEMENTS.get(course_id, {})


def get_lesson_enhancement(lesson_id):
    """获取课时增强内容"""
    return LESSON_ENHANCEMENTS.get(lesson_id, {})


def get_learning_tools():
    """获取通用学习工具"""
    return LEARNING_TOOLS
