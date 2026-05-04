# -*- coding: utf-8 -*-
"""Script to update EXAM_QUESTIONS in course_data.py for exams 1-6"""

import re

# Read the current file
with open('course_data.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the EXAM_QUESTIONS section
exam_q_start = content.find('EXAM_QUESTIONS = [')
exam7_marker = '# Exam 7: Python综合能力考核 (57题'
exam7_pos = content.find(exam7_marker)
exam_q_end = content.rfind(']')

# Extract pre-EXAM_QUESTIONS content (COURSES, LESSONS, EXERCISES, EXAMS)
pre_content = content[:exam_q_start]

# Extract Exam 7 section (keep as-is)
exam7_content = content[exam7_pos:]

# Now build new EXAM_QUESTIONS for exams 1-6
# Each exam: 57 questions (30 single_choice + 10 true_false + 8 fill_blank + 4 code_reading + 3 short_answer + 2 programming)

new_questions = []

def add_q(exam, qtype, text, options, answer, points, order, difficulty, knowledge_point, lesson_id=0):
    new_questions.append({
        'exam': exam, 'type': qtype, 'text': text, 'options': options,
        'answer': answer, 'points': points, 'order': order,
        'difficulty': difficulty, 'knowledge_point': knowledge_point, 'lesson_id': lesson_id
    })

# ==========================================================
# Exam 1: Python基础入门测试 (57题)
# ==========================================================
e = 1  # exam_id

# --- 单选题 (30题, 各1.5分) ---
sc = [
    ("Python语言由谁创建？","A. James Gosling  B. Guido van Rossum  C. Dennis Ritchie  D. Bjarne Stroustrup","B","easy","Python历史"),
    ("以下哪个不是Python的主要特点？","A. 解释型语言  B. 静态类型语言  C. 跨平台  D. 丰富的标准库","B","easy","Python特点"),
    ("以下哪个是有效的Python变量名？","A. 2name  B. my-name  C. _name  D. class","C","easy","变量命名"),
    ("表达式 type(3.14) 的结果是？","A. &lt;class 'int'&gt;  B. &lt;class 'float'&gt;  C. &lt;class 'str'&gt;  D. &lt;class 'double'&gt;","B","easy","数据类型"),
    ("Python中用于输出的内置函数是？","A. printf()  B. echo()  C. print()  D. display()","C","easy","输出函数"),
    ("表达式 17 // 5 的结果是？","A. 3.4  B. 3  C. 2  D. 4","B","easy","整除运算"),
    ("以下哪个不是Python内置的数据类型？","A. int  B. float  C. char  D. bool","C","easy","数据类型"),
    ("字符串 'Hello' + 'World' 的结果是？","A. 'Hello World'  B. 'HelloWorld'  C. 'Hello+World'  D. 报错","B","easy","字符串拼接"),
    ("以下哪个符号表示Python中的单行注释？","A. //  B. #  C. /*  D. --","B","easy","注释"),
    ("Python中用于获取用户输入的函数是？","A. scan()  B. read()  C. input()  D. get()","C","easy","输入函数"),
    ("表达式 3 * 'ab' 的结果是？","A. '3ab'  B. 'ababab'  C. 'ab3'  D. 报错","B","medium","字符串乘法"),
    ("以下哪个关键字用于定义函数？","A. func  B. def  C. function  D. define","B","easy","函数定义"),
    ("range(2, 8, 2) 生成的序列是？","A. [2,4,6,8]  B. [2,4,6]  C. [2,3,4,5,6,7]  D. [2,4,8]","B","medium","range函数"),
    ("Python三目表达式的正确写法是？","A. x > 0 ? '正' : '负'  B. '正' if x > 0 else '负'  C. x > 0 : '正' ? '负'  D. if x > 0 then '正' else '负'","B","easy","三元表达式"),
    ("在Python中，以下哪个值在条件判断中为False？","A. 1  B. 'False'  C. []  D. (1,)","C","medium","布尔判断"),
    ("以下哪个方法可以向列表末尾添加元素？","A. add()  B. insert()  C. extend()  D. append()","D","easy","列表操作"),
    ("字符串方法 'hello'.upper() 的结果是？","A. 'Hello'  B. 'HELLO'  C. 'hello'  D. 报错","B","easy","字符串方法"),
    ("以下哪个运算符用于取模（求余数）？","A. /  B. %  C. //  D. **","B","easy","算术运算符"),
    ("表达式 2 ** 3 的结果是？","A. 6  B. 8  C. 9  D. 5","B","easy","幂运算"),
    ("for i in range(5) 循环执行的次数是？","A. 4  B. 5  C. 6  D. 无限","B","easy","for循环"),
    ("以下哪个关键字用于导入模块？","A. from  B. include  C. require  D. using","A","easy","模块导入"),
    ("列表 [1,2,3] + [4,5] 的结果是？","A. [1,2,3,[4,5]]  B. [1,2,3,4,5]  C. [5,7,5]  D. 报错","B","medium","列表拼接"),
    ("Python中变量命名不能以什么开头？","A. 字母  B. 下划线  C. 数字  D. 大写字母","C","easy","变量命名规则"),
    ("以下哪个不是Python的算术运算符？","A. +  B. //  C. **  D. &&","D","easy","运算符"),
    ("下列代码的输出结果是？\nx = 5\ny = x\ny = 3\nprint(x)","A. 3  B. 5  C. 0  D. Error","B","medium","变量赋值"),
    ("以下哪个是正确的f-string写法？","A. f'Hello {name}'  B. f'Hello {{name}}'  C. f\"Hello name\"  D. 'Hello {name}'","A","medium","f-string格式化"),
    ("在循环中，哪个语句用于提前终止整个循环？","A. break  B. continue  C. return  D. exit","A","easy","break语句"),
    ("以下哪个模块提供了数学函数？","A. numbers  B. math  C. calc  D. num","B","easy","math模块"),
    ("表达式 len('Python') 的结果是？","A. 5  B. 6  C. 7  D. 0","B","easy","len函数"),
    ("以下哪个符号表示Python中的逻辑与？","A. &&  B. &  C. and  D. AND","C","medium","逻辑运算符"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

# --- 判断题 (10题, 各1分) ---
tf = [
    ("Python是静态类型语言。","false","easy","Python特点"),
    ("Python中的变量可以直接赋值使用，不需要声明类型。","true","easy","变量声明"),
    ("range(5)生成的是0到4的整数序列。","true","easy","range函数"),
    ("Python中的字符串可以使用单引号或双引号表示。","true","easy","字符串"),
    ("在Python中，x = y = 10 是错误的语法。","false","medium","多重赋值"),
    ("使用import可以导入Python标准库。","true","easy","模块导入"),
    ("if语句后面必须跟else语句。","false","medium","条件语句"),
    ("Python中列表(list)创建后可以修改其中的元素。","true","easy","列表特性"),
    ("函数return语句必须返回一个值。","false","medium","函数返回"),
    ("len()函数可以获取列表、字符串和字典的长度。","true","medium","内置函数"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

# --- 填空题 (8题, 各1.5分) ---
fb = [
    ("将字符串'123'转换为整数的函数是________。","int()","easy","类型转换"),
    ("Python中用于获取用户输入的内置函数是________。","input()","easy","输入函数"),
    ("在循环中跳过本次迭代继续下一次的关键字是________。","continue","easy","循环控制"),
    ("以下代码的输出结果是：\nx = 10\ny = 3\nprint(x % y)\n答：________","1","medium","取模运算"),
    ("以下代码的输出结果是：\ndef add(a=5, b=10):\n    return a + b\nprint(add(3))\n答：________","13","medium","默认参数"),
    ("以下代码的输出结果是：\nprint(2 ** 3 ** 2)\n答：________","512","hard","幂运算优先级"),
    ("使用________函数可以查看对象的类型。","type()","easy","type函数"),
    ("以下代码的输出结果是：\ntext = 'Python'\nprint(text[::-1])\n答：________","nohtyP","medium","字符串切片"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

# --- 程序阅读题 (4题, 各3分) ---
cr = [
    ("阅读以下代码，输出结果是什么？\n\nx = 10\ny = 3\nprint(x % y, x // y, x / y)","A. 1 3 3.333  B. 1 3 3  C. 3 1 3.333  D. 3 1 3","A","medium","运算符综合"),
    ("阅读以下代码，输出结果是什么？\n\nscore = 85\nif score >= 90:\n    g = 'A'\nelif score >= 80:\n    g = 'B'\nelif score >= 70:\n    g = 'C'\nelse:\n    g = 'D'\nprint(g)","A. A  B. B  C. C  D. D","B","medium","if-elif结构"),
    ("阅读以下代码，输出结果是什么？\n\nresult = 0\nfor i in range(1, 6):\n    if i % 2 == 0:\n        result += i\n    else:\n        result -= i\nprint(result)","A. -3  B. 3  C. 0  D. -1","A","hard","循环与条件"),
    ("阅读以下代码，输出结果是什么？\n\ndef func(a, b=2, *args):\n    return a + b + sum(args)\nprint(func(1, 3, 4, 5))","A. 10  B. 13  C. 6  D. 15","B","hard","函数参数综合"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

# --- 简答题 (3题, 各3分) ---
sa = [
    ("请简述break和continue在循环中的区别。","break用于完全终止循环，程序继续执行循环外的代码；continue用于跳过当前迭代的剩余代码，直接进入下一次循环判断。","medium","循环控制"),
    ("请解释函数的默认参数的作用，并说明使用默认参数时的注意事项。","默认参数允许函数调用时不传某些参数而使用预定义值。注意事项：默认参数应该是不变对象（如None、字符串、数字），避免使用可变对象（如列表）作为默认值，因为默认值在函数定义时计算一次。","hard","默认参数"),
    ("请简述Python中深拷贝与浅拷贝的区别。","浅拷贝只复制对象本身，内部元素仍引用原对象；深拷贝会递归复制所有层级的对象，生成完全独立的副本。","medium","拷贝机制"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

# --- 编程题 (2题, 各6分) ---
pr = [
    ("编写一个函数 is_prime(n)，判断一个正整数是否为素数。素数是指只能被1和自身整除的大于1的整数。返回True或False。","def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5)+1):\n        if n % i == 0:\n            return False\n    return True","medium","素数判断"),
    ("编写一个函数 calc_stats(numbers)，接收一个数字列表，返回一个包含最大值、最小值、平均值和总和的元组。\n例：calc_stats([1,2,3,4,5]) -> (5, 1, 3.0, 15)","def calc_stats(numbers):\n    total = sum(numbers)\n    avg = total / len(numbers)\n    return (max(numbers), min(numbers), avg, total)","medium","列表统计"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ==========================================================
# Exam 2: Python数据结构测试 (57题)
# ==========================================================
e = 2

sc = [
    ("列表 nums = [1,2,3,4] 中，nums[-1] 的值是？","A. 1  B. 4  C. Error  D. 0","B","easy","列表索引"),
    ("以下哪个方法能在列表末尾添加元素？","A. add()  B. insert()  C. extend()  D. append()","D","easy","列表操作"),
    ("列表切片 lst[1:4] 对 lst=[0,1,2,3,4,5] 的结果是？","A. [0,1,2,3]  B. [1,2,3,4]  C. [1,2,3]  D. [0,1,2,3,4]","C","easy","列表切片"),
    ("以下哪个是创建单元素元组的正确方式？","A. (1)  B. (1,)  C. [1]  D. {1}","B","easy","元组"),
    ("字典中安全获取值的方法是？","A. dict[key]  B. dict.get(key, default)  C. dict.find(key)  D. dict.value(key)","B","easy","字典"),
    ("集合 {1, 2, 2, 3, 3, 3} 的实际值是？","A. {1, 2, 2, 3, 3, 3}  B. {1, 2, 3}  C. [1, 2, 3]  D. 报错","B","easy","集合去重"),
    ("以下哪个不能作为字典的键？","A. 字符串  B. 数字  C. 列表  D. 元组","C","medium","字典键"),
    ("以下哪个运算符表示集合的交集？","A. |  B. &  C. -  D. ^","B","easy","集合运算"),
    ("列表推导式 [x**2 for x in range(5)] 的结果是？","A. [0,1,4,9,16]  B. [1,4,9,16,25]  C. (0,1,4,9,16)  D. {0,1,4,9,16}","A","easy","列表推导式"),
    ("以下哪个数据结构是有序的？","A. 集合  B. 字典(Python 3.7+)  C. 数学集合  D. frozenset","B","medium","字典顺序"),
    ("元组与列表的主要区别是？","A. 元组用()，列表用[]  B. 元组不可变，列表可变  C. 元组不能为空  D. 以上都不对","B","easy","元组vs列表"),
    ("以下哪个方法可以删除列表中指定值的元素？","A. pop()  B. remove()  C. delete()  D. clear()","B","easy","列表删除"),
    ("字符串 'hello'[1:4] 的结果是？","A. 'ell'  B. 'hel'  C. 'ello'  D. 'h'","A","medium","字符串切片"),
    ("字典推导式 {x:x**2 for x in range(3)} 的结果是？","A. {0:0,1:1,2:4}  B. {1:1,2:4,3:9}  C. [0,1,4]  D. {0,1,4}","A","medium","字典推导式"),
    ("以下哪个方法可以合并两个字典？","A. merge()  B. combine()  C. update()  D. join()","C","medium","字典合并"),
    ("set() 函数可以用来？","A. 创建空字典  B. 创建空集合  C. 创建空列表  D. 创建空元组","B","easy","集合创建"),
    ("以下哪个方法用于在列表中指定位置插入元素？","A. append()  B. extend()  C. insert()  D. push()","C","easy","列表插入"),
    ("collections.deque 最适合实现什么数据结构？","A. 栈  B. 队列  C. 堆  D. 树","B","medium","deque队列"),
    ("以下哪个操作会改变原列表？","A. sorted(lst)  B. lst[::-1]  C. lst.sort()  D. [x*2 for x in lst]","C","medium","sort vs sorted"),
    ("Python中字符串是否可变？","A. 可变  B. 不可变  C. 视情况而定  D. Python 3中可变","B","easy","字符串不可变"),
    ("以下哪种数据类型可以用于列表去重？","A. 列表  B. 元组  C. 字典  D. 集合","D","easy","集合应用"),
    ("join() 方法是哪个数据类型的方法？","A. 列表  B. 元组  C. 字符串  D. 集合","C","medium","字符串方法"),
    ("以下哪个集合运算用于获取两个集合的并集？","A. &  B. |  C. -  D. ^","B","easy","集合并集"),
    ("sorted(lst, reverse=True) 的排序结果是？","A. 升序  B. 降序  C. 随机  D. 保持原样","B","easy","排序"),
    ("以下哪个方法用于清空列表？","A. remove()  B. delete()  C. clear()  D. drop()","C","easy","列表清空"),
    ("Python中，为什么集合的元素必须是不可变的？","A. 因为集合使用哈希表  B. 因为集合是有序的  C. 因为集合限制大小  D. 以上都不对","A","hard","集合原理"),
    ("列表 lst.extend([4,5]) 的效果是？","A. 将[4,5]作为单个元素加入  B. 将4和5逐个加入列表尾  C. 替换列表  D. 报错","B","medium","extend方法"),
    ("以下哪种方式可以同时遍历两个列表？","A. enumerate()  B. range()  C. zip()  D. map()","C","easy","zip函数"),
    ("Python中 a = [1,2]; b = a; b[0] = 9; print(a[0]) 输出是？","A. 1  B. 9  C. Error  D. 2","B","medium","列表引用"),
    ("字典的 values() 方法返回什么？","A. 键列表  B. 值视图对象  C. 元组  D. 集合","B","medium","values方法"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

tf = [
    ("列表是可变的，元组是不可变的。","true","easy","可变性"),
    ("集合中的元素是有序的。","false","easy","集合无序"),
    ("字典的键(key)必须是不可变类型。","true","easy","字典键"),
    ("使用 {} 可以创建一个空集合。","false","easy","集合创建"),
    ("Python的列表支持负索引。","true","easy","列表索引"),
    ("字符串的upper()方法会修改原字符串。","false","medium","字符串方法"),
    ("使用collections.Counter可以方便地统计元素频率。","true","medium","Counter"),
    ("元组解包时，左侧变量数必须与元组长度严格相等。","false","medium","元组解包"),
    ("集合中的元素不能重复。","true","easy","集合特性"),
    ("shallow copy（浅拷贝）会完全复制嵌套列表的子列表。","false","hard","拷贝"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

fb = [
    ("使用________函数可以获取列表的长度。","len()","easy","列表长度"),
    ("将元组 t = (1, 2, 3) 转换为列表使用________方法。","list()","easy","类型转换"),
    ("以下代码的输出结果是：\n' '.join(['Hello', 'Python'])\n答：________","Hello Python","medium","join方法"),
    ("以下代码的输出结果是：\na = [1,2,3]; a.pop(1)\nprint(a)\n答：________","[1, 3]","medium","pop方法"),
    ("以下代码的输出结果是：\nd = {'a':1,'b':2}\nprint(d.get('c', 0))\n答：________","0","easy","字典get"),
    ("以下代码的输出结果是：\nprint(sorted([3,1,2],reverse=True))\n答：________","[3, 2, 1]","medium","sorted排序"),
    ("以下代码的输出结果是：\ns = {1,2,3} & {2,3,4}\nprint(len(s))\n答：________","2","medium","集合交集"),
    ("使用collections模块的________类可以方便地实现队列。","deque","medium","deque"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

cr = [
    ("阅读以下代码，输出结果是什么？\n\na = [1,2,3]\nb = a\nc = a.copy()\na.append(4)\nprint(len(b), len(c))","A. 3 3  B. 4 3  C. 4 4  D. 3 4","B","hard","列表引用与拷贝"),
    ("阅读以下代码，输出结果是什么？\n\nd = {'a':1,'b':2}\nd.update({'b':3,'c':4})\nprint(d['b'], len(d))","A. 2 2  B. 3 3  C. 2 3  D. 3 2","B","medium","update方法"),
    ("阅读以下代码，输出结果是什么？\n\na = {1,2,3,4}\nb = {3,4,5,6}\nprint(len(a ^ b))","A. 2  B. 4  C. 6  D. 0","B","hard","对称差集"),
    ("阅读以下代码，输出结果是什么？\n\ncounts = {}\ntext = 'hello world hello'\nfor w in text.split():\n    counts[w] = counts.get(w, 0) + 1\nprint(counts['hello'])","A. 1  B. 2  C. 0  D. Error","B","medium","词频统计"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

sa = [
    ("请简述Python中列表与元组的主要区别及适用场景。","主要区别：列表(list)是可变的，可以增删改元素；元组(tuple)是不可变的。适用场景：列表用于需要动态修改的数据集合（如待办事项列表）；元组用于不希望被修改的固定数据（如坐标、配置常量），且元组可作为字典的键。","easy","列表vs元组"),
    ("请简述Python中集合(set)的工作原理及适用场景。","集合基于哈希表实现，元素必须是不可变(hashable)类型。特点是：元素不重复、无序、支持数学集合运算（并交差）。适用场景：数据去重（如去除重复项）、成员关系快速判断（in操作O(1)）、数学集合运算（查找共同元素等）。","medium","集合原理"),
    ("解释深拷贝（deep copy）与浅拷贝（shallow copy）的区别，举例说明。","浅拷贝只复制容器本身，容器内的元素仍引用原对象的元素；深拷贝递归复制所有层级对象。例：a = [[1,2],[3,4]]; b = a.copy()（浅拷贝），修改b[0][0]会影响a；c = copy.deepcopy(a)（深拷贝），修改c[0][0]不影响a。","hard","深浅拷贝"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

pr = [
    ("编写一个函数 flatten(lst)，接收一个嵌套列表，返回一个扁平化的一维列表。嵌套深度不限。\n例：flatten([1,[2,[3,4]],5]) -> [1,2,3,4,5]","def flatten(lst):\n    result = []\n    for item in lst:\n        if isinstance(item, list):\n            result.extend(flatten(item))\n        else:\n            result.append(item)\n    return result","hard","递归扁平化"),
    ("编写一个函数 most_frequent(lst)，接收一个列表，返回出现频率最高的元素及出现次数。如果多个元素频率相同，返回任意一个。\n例：most_frequent([1,2,2,3,3,3]) -> (3, 3)","def most_frequent(lst):\n    from collections import Counter\n    c = Counter(lst)\n    return c.most_common(1)[0]","medium","词频统计"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ==========================================================
# Exam 3: 面向对象编程测试 (57题)
# ==========================================================
e = 3

sc = [
    ("Python中类的构造函数名称是？","A. __construct__  B. __init__  C. __new__  D. __create__","B","easy","构造函数"),
    ("实例方法中第一个参数通常命名为？","A. this  B. self  C. cls  D. me","B","easy","self参数"),
    ("在子类中调用父类方法应使用？","A. parent()  B. base()  C. super()  D. ancestor()","C","easy","super函数"),
    ("以下哪个魔术方法用于print输出对象？","A. __repr__  B. __str__  C. __print__  D. __format__","B","easy","__str__方法"),
    ("@property装饰器的作用是？","A. 定义类方法  B. 将方法转换为属性访问  C. 定义静态方法  D. 声明抽象方法","B","easy","property装饰器"),
    ("以下哪个不是面向对象的三大特性？","A. 封装  B. 继承  C. 多态  D. 递归","D","easy","OOP特性"),
    ("Python中关于self说法正确的是？","A. self是关键字  B. self代表类的实例本身  C. self只能在__init__中使用  D. self必须声明类型","B","easy","self含义"),
    ("以下哪个是定义抽象基类的正确方式？","A. class MyClass(Base):  B. class MyClass(ABC):  C. class MyClass(abstract):  D. abstract class MyClass:","B","medium","抽象基类"),
    ("以下哪个关键字用于创建一个子类继承父类？","A. extends  B. inherits  C. 括号中指定父类  D. @inherit","C","easy","继承语法"),
    ("类方法装饰器是？","A. @staticmethod  B. @classmethod  C. @property  D. @abstractmethod","B","easy","类方法"),
    ("OOP中封装的主要目的是？","A. 隐藏实现细节  B. 加速代码运行  C. 创建更多类  D. 替代函数","A","medium","封装"),
    ("面向对象的单一职责原则指的是？","A. 每个类只负责一项职责  B. 每个类只有一个方法  C. 每个类只有一个实例  D. 以上都不对","A","medium","单一职责"),
    ("以下哪个关于继承的正确描述？","A. 子类不能访问父类方法  B. 子类可以重写父类方法  C. 子类不能有自己的属性  D. Python不支持多重继承","B","easy","继承"),
    ("Python的多继承使用什么算法解决顺序？","A. DFS  B. BFS  C. C3线性化(MRO)  D. 随机","C","hard","MRO算法"),
    ("以下哪个不是魔术方法？","A. __init__  B. __str__  C. __private__  D. __len__","C","medium","魔术方法"),
    ("类属性和实例属性的区别是？","A. 类属性所有实例共享  B. 两者完全相同  C. 类属性是私有的  D. 实例属性不能在__init__中定义","A","medium","属性区别"),
    ("以下哪个装饰器将方法转换为属性？","A. @property  B. @attribute  C. @method  D. @field","A","easy","property"),
    ("Python中使用什么实现多态？","A. 函数重载  B. 方法签名不同  C. 鸭子类型(Duck Typing)  D. 接口声明","C","hard","多态"),
    ("以下哪个可以限制实例属性的添加？","A. __slots__  B. __attr__  C. __limit__  D. __restrict__","A","hard","__slots__"),
    ("静态方法装饰器是？","A. @staticmethod  B. @classmethod  C. @property  D. @abstractmethod","A","easy","静态方法"),
    ("以下哪个设计原则强调'对扩展开放，对修改关闭'？","A. 单一职责  B. 开闭原则  C. 里氏替换  D. 依赖倒置","B","medium","SOLID"),
    ("Python中以下划线开头的属性名表示？","A. 公有属性  B. 私有属性(约定)  C. 魔术属性  D. 必须属性","B","medium","命名约定"),
    ("关于Python中的抽象基类，正确的是？","A. 可以直接实例化  B. 必须实现所有抽象方法才能实例化  C. Python不支持抽象类  D. 抽象方法用@virtual声明","B","hard","抽象基类"),
    ("以下哪个方法定义了对象相等比较？","A. __eq__  B. __equal__  C. __equals__  D. __compare__","A","medium","比较魔术方法"),
    ("自定义类实现len()需要定义哪个方法？","A. __getitem__  B. __length__  C. __size__  D. __len__","D","medium","__len__方法"),
    ("Python中的'鸭子类型'概念是什么？","A. 对象的类型由其行为决定  B. 只能处理鸭子对象  C. 必须显式声明接口  D. 以上都不对","A","hard","鸭子类型"),
    ("以下关于Python类的说法错误的是？","A. 类定义了对象的模板  B. 一个类可以有多个实例  C. Python中没有继承的概念  D. 类中的方法可以访问实例属性","C","easy","类基础"),
    ("以下哪个可以定义'只读'属性？","A. 只用@property定义getter  B. 只用@property定义setter  C. 不能用只读属性  D. 类中没法实现","A","medium","只读属性"),
    ("关于Python中isinstance()函数说法正确的是？","A. 检查对象类型  B. 创建实例  C. 删除实例  D. 复制对象","A","easy","isinstance"),
    ("依赖倒置原则的核心思想是？","A. 依赖具体类  B. 高层模块不应依赖低层模块，两者都应依赖抽象  C. 低层依赖高层  D. 模块间不需要依赖","B","hard","依赖倒置"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

tf = [
    ("Python支持多重继承。","true","easy","多重继承"),
    ("__init__方法在对象销毁时被调用。","false","easy","__init__"),
    ("Python中self参数可以省略。","false","easy","self"),
    ("子类可以访问父类的所有公共方法。","true","easy","继承"),
    ("静态方法可以访问实例属性。","false","medium","静态方法"),
    ("Python的方法解析顺序使用C3线性化算法。","true","hard","MRO"),
    ("使用@property装饰器可以将方法调用变为属性访问。","true","medium","property"),
    ("Python中没有访问控制，所有属性都是公开的。","false","medium","访问控制"),
    ("@classmethod定义的方法第一个参数是self。","false","medium","类方法"),
    ("多态允许不同类的对象对相同方法调用做出不同响应。","true","medium","多态"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

fb = [
    ("在Python类中，构造方法名为________。","__init__","easy","构造方法"),
    ("使用super()调用父类方法，传参格式为 super().__init__(...)；而类方法中第一个参数应命名为________。","cls","medium","类方法"),
    ("以下代码的输出结果是：\nclass Dog:\n    sound = 'woof'\nprint(Dog.sound)\n答：________","woof","easy","类属性"),
    ("以下代码的输出结果是：\nclass A:\n    def f(self):\n        return 'A'\nclass B(A):\n    def f(self):\n        return 'B' + super().f()\nprint(B().f())\n答：________","BA","hard","super调用"),
    ("Python中实现名称修饰（Name Mangling），双下划线前缀的属性会被重命名为________。","_ClassName__attr","hard","名称修饰"),
    ("以下代码的输出结果是：\nclass C:\n    count = 0\n    def __init__(self):\n        C.count += 1\nc1 = C()\nprint(C.count)\n答：________","1","medium","类属性共享"),
    ("使用________模块的ABC类和abstractmethod装饰器可以定义抽象基类。","abc","medium","abc模块"),
    ("以下代码的输出结果是：\nclass Book:\n    def __init__(self, title):\n        self.title = title\n    def __str__(self):\n        return self.title\nprint(Book('Python'))\n答：________","Python","medium","__str__"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

cr = [
    ("阅读以下代码，输出结果是什么？\n\nclass Animal:\n    def speak(self):\n        return 'animal'\n\nclass Dog(Animal):\n    def speak(self):\n        return 'woof'\n\nclass Cat(Animal):\n    def speak(self):\n        return 'meow'\n\nanimals = [Dog(), Cat(), Animal()]\nfor a in animals:\n    print(a.speak(), end=' ')","A. woof meow animal  B. animal animal animal  C. woof woof woof  D. 报错","A","hard","多态"),
    ("阅读以下代码，输出结果是什么？\n\nclass A:\n    def m(self):\n        return 'A'\n\nclass B(A):\n    def m(self):\n        return 'B' + super().m()\n\nclass C(B):\n    def m(self):\n        return 'C' + super().m()\n\nprint(C().m())","A. CBA  B. C  C. A  D. Error","A","hard","继承链"),
    ("阅读以下代码，指出违反了什么原则。\n\nclass Report:\n    def gen(self): pass\n    def save(self): pass\n    def email(self): pass","A. 单一职责原则  B. 开闭原则  C. 里氏替换原则  D. 没有违反","A","medium","设计原则"),
    ("阅读以下代码，输出结果是什么？\n\nclass Dog:\n    kind = 'canine'\n    def __init__(self, name):\n        self.name = name\n\nd1 = Dog('Fido')\nd1.kind = 'pet'\nprint(Dog.kind)","A. canine  B. pet  C. None  D. Error","A","hard","类属性vs实例属性"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

sa = [
    ("请简述面向对象三大特性：封装、继承和多态。","封装：隐藏内部实现细节，只暴露必要的接口，提高安全性和可维护性。继承：子类可以重用父类的属性和方法，并扩展新功能，实现代码复用。多态：同一个方法在不同类中可以有不同实现，调用者无需关心具体类型，鸭子类型即可。","medium","OOP三大特性"),
    ("请简述SOLID设计原则中至少三个原则的含义。","单一职责：一个类只负责一项职责。开闭原则：对扩展开放，对修改关闭。里氏替换：子类应该可以替换父类而不影响程序正确性。依赖倒置：高层模块不应依赖低层模块，两者都应依赖抽象。","hard","SOLID"),
    ("请简述Python中@property装饰器的用途和使用方式。","@property可以将类的方法转换为属性访问，使得可以通过 obj.attr 方式调用。通过@property定义getter（只读），@attr.setter定义setter。适用于：计算属性（如温度转换摄氏度到华氏度）、数据验证（设置值时检查合法性）、封装实现细节。","medium","property"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

pr = [
    ("编写一个Python类 Stack，实现栈的基本操作：push（入栈）、pop（出栈）、peek（查看栈顶）、is_empty（判断是否为空）、size（返回元素个数）。","class Stack:\n    def __init__(self):\n        self.items = []\n    def push(self, item):\n        self.items.append(item)\n    def pop(self):\n        if not self.is_empty():\n            return self.items.pop()\n        raise IndexError('Stack is empty')\n    def peek(self):\n        if not self.is_empty():\n            return self.items[-1]\n        raise IndexError('Stack is empty')\n    def is_empty(self):\n        return len(self.items) == 0\n    def size(self):\n        return len(self.items)","medium","栈实现"),
    ("编写一个Python类 BankAccount，具有属性 owner(姓名) 和 balance(余额)，方法 deposit(amount) 存款、withdraw(amount) 取款（余额不足时报错），以及 get_balance() 返回余额。","class BankAccount:\n    def __init__(self, owner, balance=0):\n        self.owner = owner\n        self._balance = balance\n    def deposit(self, amount):\n        if amount <= 0:\n            raise ValueError('Amount must be positive')\n        self._balance += amount\n        return self._balance\n    def withdraw(self, amount):\n        if amount <= 0:\n            raise ValueError('Amount must be positive')\n        if amount > self._balance:\n            raise ValueError('Insufficient funds')\n        self._balance -= amount\n        return self._balance\n    def get_balance(self):\n        return self._balance","medium","银行账户类"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ==========================================================
# Exam 4: 文件操作与异常处理测试 (57题)
# ==========================================================
e = 4

sc = [
    ("以下哪个模式以追加方式打开文件？","A. r  B. w  C. a  D. x","C","easy","文件模式"),
    ("with open() as f 语句中，文件何时自动关闭？","A. 程序结束  B. with块结束时  C. 对象销毁  D. 手动调用close()","B","easy","上下文管理"),
    ("以下哪个不是文件读取方法？","A. read()  B. readline()  C. write()  D. readlines()","C","easy","文件方法"),
    ("以下哪个异常在除以零时抛出？","A. ValueError  B. TypeError  C. ZeroDivisionError  D. ArithmeticError","C","easy","异常类型"),
    ("try-except中else子句何时执行？","A. 始终执行  B. 异常时执行  C. 无异常时执行  D. 永远不会","C","easy","else子句"),
    ("以下哪个函数将Python字典转为JSON字符串？","A. json.loads()  B. json.dumps()  C. json.read()  D. json.write()","B","easy","JSON序列化"),
    ("csv模块中哪个类写入CSV字典数据？","A. csv.writer  B. csv.DictWriter  C. csv.DictReader  D. csv.Writer","B","easy","CSV写入"),
    ("shutil.copy2()的主要特性是？","A. 复制目录  B. 保留元数据  C. 速度更快  D. 支持网络","B","medium","shutil"),
    ("以下哪个直接能被JSON序列化？","A. set  B. tuple  C. dict  D. bytes","C","medium","JSON类型"),
    ("自定义异常需继承哪个类？","A. Error  B. Exception  C. RuntimeException  D. Base","B","medium","自定义异常"),
    ("以下哪个json.dumps参数保留中文不转义？","A. indent=2  B. sort_keys=True  C. ensure_ascii=False  D. ensure_unicode=True","C","easy","JSON中文"),
    ("os.path.join()函数的作用是？","A. 拼接路径  B. 拆分路径  C. 查询文件  D. 删除文件","A","easy","路径拼接"),
    ("以下哪个模式以二进制读取打开文件？","A. 'r'  B. 'rb'  C. 'w'  D. 'a'","B","medium","二进制模式"),
    ("f.readlines()方法返回什么？","A. 字符串  B. 列表  C. 字典  D. 迭代器","B","easy","readlines"),
    ("哪个异常类型在访问字典不存在的键时抛出？","A. IndexError  B. TypeError  C. KeyError  D. ValueError","C","easy","KeyError"),
    ("在try-except-finally结构中，finally何时执行？","A. 异常时  B. 正常时  C. 总是执行  D. 不执行","C","medium","finally子句"),
    ("os.makedirs(path, exist_ok=True)的含义是？","A. 总是覆盖  B. 存在时跳过  C. 存在时报错  D. 删除重新创建","B","medium","目录创建"),
    ("以下哪个函数直接读JSON文件并返回Python对象？","A. json.dumps()  B. json.loads()  C. json.load()  D. json.dump()","C","medium","JSON文件读取"),
    ("使用＿＿可以安全获取嵌套字典的值？","A. d[key][key]  B. d.get(key,{})  C. d.find(key)  D. d.search(key)","B","medium","嵌套字典"),
    ("csv.reader()返回的是什么？","A. DictReader对象  B. 迭代器对象  C. 字典  D. 字符串","B","medium","CSV reader"),
    ("以下哪行能正确处理文件编码？","A. open('f.txt')  B. open('f.txt', 'r', encoding='utf-8')  C. read('f.txt')  D. fopen('f.txt')","B","easy","编码"),
    ("以下哪个内置函数可以检测文件是否存在？","A. os.isFile()  B. os.path.exists()  C. os.exist()  D. os.fileExists()","B","medium","文件检测"),
    ("程序抛异常且未被捕获，将会？","A. 正常运行  B. 程序崩溃  C. 自动重启  D. 忽略","B","easy","未捕获异常"),
    ("json.loads()接收到非法JSON会抛什么异常？","A. KeyError  B. JSONDecodeError  C. ValueError  D. SyntaxError","B","hard","JSON异常"),
    ("使用csv.DictReader读取CSV，每行返回什么？","A. OrderedDict  B. 列表  C. 元组  D. 字符串","A","medium","DictReader"),
    ("readline()和readlines()的主要区别？","A. 返回类型  B. 读取速度  C. 编码方式  D. 文件大小","A","easy","读取区别"),
    ("json.dumps(data, indent=2)中indent的作用？","A. 格式化缩进输出  B. 限制字段  C. 忽略字段  D. 压缩输出","A","easy","JSON美化"),
    ("Python文件操作推荐使用with语句的主要原因是？","A. 代码美观  B. 自动调用close()释放资源  C. 运行更快  D. 支持更多功能","B","easy","with语句"),
    ("引发异常使用哪个关键字？","A. throw  B. raise  C. error  D. except","B","easy","raise"),
    ("os.listdir('.')返回什么？","A. 所有文件列表(含子目录)  B. 仅文件名  C. 目录树  D. 文件内容","A","easy","listdir"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

tf = [
    ("Python中打开文件必须指定编码格式。","false","easy","文件编码"),
    ("with open() 文件会在with块退出时自动关闭。","true","easy","自动关闭"),
    ("json.loads() 可以将JSON字符串转换为Python字典。","true","easy","json.loads"),
    ("try语句块后面必须至少有一个except或finally。","false","medium","try异常"),
    ("csv.DictWriter需要指定fieldnames参数。","true","medium","DictWriter"),
    ("os.makedirs('path', exist_ok=True) 在目录存在时不报错。","true","medium","makedirs"),
    ("except Exception: 可以捕获所有类型的异常。","true","medium","广义异常"),
    ("readlines()会将整个文件一次性全部读入内存。","true","medium","readlines"),
    ("json.dumps()可以直接序列化自定义类对象。","false","hard","JSON序列化"),
    ("Python的finally子句即使在函数中遇到return也会执行。","true","hard","finally"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

fb = [
    ("使用_________模块可以复制文件和目录。","shutil","easy","shutil模块"),
    ("打开二进制文件需使用模式参数_________。","rb","easy","二进制模式"),
    ("以下代码的输出结果是：\nimport os\nprint(os.path.join('a','b','c'))\n答：________","a/b/c","easy","路径拼接"),
    ("以下代码的输出结果是：\ntry:\n    x = 1/0\nexcept ZeroDivisionError:\n    print('错误')\n答：________","错误","easy","异常捕获"),
    ("以下代码的输出结果是：\nimport json\nd = {'a':1}\nprint(type(json.dumps(d)))\n答：________","str","medium","JSON类型"),
    ("csv.DictWriter中，函数________用于写入表头。","writeheader()","medium","CSV表头"),
    ("以下代码的输出结果是：\nwith open('test.txt','w') as f:\n    f.write('Hello')\nwith open('test.txt','r') as f:\n    print(f.read())\n答：________","Hello","easy","文件读写"),
    ("自定义异常类CustomError需继承自________。","Exception","easy","继承异常"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

cr = [
    ("阅读以下代码，输出结果是什么？\n\ndef divide(a, b):\n    try:\n        return a / b\n    except ZeroDivisionError:\n        return '除零'\n    except TypeError:\n        return '类型错'\n    finally:\n        print('done')\n\nprint(divide(10, 2))","A. 5.0  B. 5.0\ndone  C. done\n5.0  D. 除零","C","hard","finally执行"),
    ("阅读以下代码，输出结果是什么？\n\nimport json\ndata = {'name':'张三','age':25}\ns = json.dumps(data, ensure_ascii=False)\np = json.loads(s)\nprint(p['name'], type(p))","A. 张三 <class 'dict'>  B. 张三 <class 'str'>  C. 报错  D. name <class 'dict'>","A","medium","JSON操作"),
    ("阅读以下代码，输出结果是什么？\n\nimport csv\nfrom io import StringIO\nc = 'n,a\n张三,25'\nr = csv.DictReader(StringIO(c))\nfor row in r:\n    print(row['n'], row['a'])","A. n a  B. 张三 25  C. n,a\n张三,25  D. Error","B","medium","DictReader"),
    ("阅读以下代码，分析潜在问题：\ndef read_conf(fn):\n    with open(fn) as f:\n        return json.load(f)\nc = read_conf('cfg.json')\nprint(c['db']['host'])","A. 文件不存在  B. JSON格式错  C. 键不存在  D. 以上都可能","D","hard","健壮性"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

sa = [
    ("请简述Python异常处理中 try-except-else-finally 的执行顺序。","try 代码块尝试执行；如果无异常发生，执行 else 块；如果有异常且except匹配到对应异常类型，执行 except 中代码；finally 块无论是否发生异常、是否被捕获、甚至在 return 语句前都会执行。","medium","异常处理流程"),
    ("请简述使用 with 语句管理文件资源的好处，以及它背后的协议机制。","好处：with语句自动管理资源（文件对象退出with块自动关闭），避免因忘记调用close()造成的资源泄露和数据丢失。背后机制：上下文管理器协议，with语句调用__enter__方法在进入时获取资源，在退出with块时自动调用__exit__方法释放资源。","medium","上下文管理器"),
    ("请简述json.dumps 和 json.dump 的主要区别。","json.dumps(obj)：将Python对象转换为JSON字符串，返回str类型字符串。json.dump(obj, file)：将Python对象转换为JSON后直接写入到文件的file对象中，不返回值。类似关系：json.loads/load 与其对应。","easy","JSON区别"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

pr = [
    ("编写函数 merge_json(file_list, output)，读取file_list中所有JSON文件，合并成一个大列表并写入output文件。","import json\ndef merge_json(file_list, output):\n    all_data = []\n    for f in file_list:\n        try:\n            with open(f, 'r', encoding='utf-8') as fh:\n                data = json.load(fh)\n                if isinstance(data, list):\n                    all_data.extend(data)\n                else:\n                    all_data.append(data)\n        except (FileNotFoundError, json.JSONDecodeError) as e:\n            print(f'Error reading {f}: {e}')\n    with open(output, 'w', encoding='utf-8') as fh:\n        json.dump(all_data, fh, ensure_ascii=False, indent=2)\n    return len(all_data)","hard","JSON合并"),
    ("编写函数 csv_to_dict(filename)，读取CSV文件，返回列表，每项为包含所有字段的字典。需处理文件不存在和空文件的情况。","import csv\ndef csv_to_dict(filename):\n    try:\n        with open(filename, 'r', encoding='utf-8-sig') as f:\n            reader = csv.DictReader(f)\n            result = []\n            for row in reader:\n                result.append(dict(row))\n            return result\n    except FileNotFoundError:\n        print(f'文件 {filename} 不存在')\n        return []","medium","CSV处理"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ==========================================================
# Exam 5: Python高级特性测试 (57题)
# ==========================================================
e = 5

sc = [
    ("以下哪个关键字定义生成器函数？","A. return  B. yield  C. generate  D. produce","B","easy","yield"),
    ("以下哪个函数用于过滤可迭代对象？","A. map  B. filter  C. reduce  D. zip","B","easy","filter"),
    ("lambda表达式最多能包含几个表达式？","A. 0  B. 1  C. 无限  D. 2","B","easy","lambda"),
    ("自定义上下文管理器需实现哪两个方法？","A. __init__/__del__  B. __enter__/__exit__  C. __open__/__close__  D. __start__/__stop__","B","easy","上下文管理器"),
    ("以下哪个模块提供正则表达式功能？","A. regex  B. re  C. pattern  D. match","B","easy","re模块"),
    ("正则表达式 \\\\d+ 匹配什么？","A. 一个数字  B. 一个或多个数字  C. 任意字符  D. 空白字符","B","easy","正则元字符"),
    ("装饰器本质上是什么？","A. 类  B. 函数  C. 模块  D. 变量","B","easy","装饰器本质"),
    ("functools.wraps 的作用是？","A. 缓存结果  B. 保留被装饰函数元信息  C. 参数检查  D. 类型转换","B","easy","wraps"),
    ("生成器表达式 (x**2 for x in range(5)) 返回什么？","A. 列表  B. 生成器对象  C. 元组  D. 集合","B","easy","生成器表达式"),
    ("以下哪个是高阶函数？","A. len()  B. type()  C. map()  D. print()","C","medium","高阶函数"),
    ("__iter__ 方法返回什么？","A. 对象本身  B. 迭代器对象  C. 列表  D. None","B","medium","迭代器协议"),
    ("以下哪个不是functools模块的功能？","A. wraps  B. lru_cache  C. partial  D. gradient","D","easy","functools"),
    ("以下哪个是正则中表示字符串结尾的符号？","A. ^  B. $  C. *  D. .","B","medium","正则定位符"),
    ("使用yield关键字定义的函数返回什么类型？","A. list  B. dict  C. generator  D. iterator","C","medium","生成器"),
    ("@staticmethod 方法中关于参数正确的是？","A. 必须有self  B. 必须有cls  C. 不需传入self或cls  D. 必须有两个参数","C","medium","静态方法"),
    ("以下哪种推导式创建字典？","A. [x:x**2 for x in range(3)]  B. {x:x**2 for x in range(3)}  C. (x:x**2 for x in range(3))  D. <x:x**2 for x in range(3)>","B","easy","字典推导式"),
    ("以下哪个集合推导式语法正确？","A. {x for x in range(5)}  B. [x for x in range(5)]  C. (x for x in range(5))  D. <x for x in range(5)>","A","medium","集合推导式"),
    ("关于闭包正确的是？","A. 闭包不能访问外部变量  B. 闭包可以记住创建时所在外部作用域变量  C. 闭包不含内部函数  D. 闭包不需要嵌套","B","hard","闭包"),
    ("关于迭代器和可迭代对象正确的是？","A. 两者完全相同  B. 可迭代对象实现__iter__()  C. 字符串不可迭代  D. 字典不是可迭代对象","B","medium","迭代器vs可迭代"),
    ("re.findall() 未匹配到任何内容时返回什么？","A. None  B. 空列表 []  C. False  D. 空字符串 ''","B","medium","findall返回"),
    ("search/match/sub/split 属于哪个模块？","A. re  B. regexp  C. pattern  D. match","A","easy","re方法"),
    ("下列语句中能正确创建生成器对象的是？","A. (x**2 for x in range(5))  B. yield 5  C. def gen(): yield   , gen()  D. generator()","C","medium","生成器创建"),
    ("非局部变量(nonlocal)关键字用于？","A. 修改全局变量  B. 修改上一层非全局变量  C. 声明私有变量  D. 声明静态变量","B","hard","nonlocal"),
    ("reduce函数位于哪个模块？","A. builtins  B. functools  C. itertools  D. operators","B","easy","reduce位置"),
    ("以下关于解包正确的是？","A. a,*b = [1,2,3]  b->[2,3]  B. a,*b = [1,2,3] b->2  C. 不支持星号解包  D. 恒使解包失败","A","medium","元组解包"),
    ("以下关于functools.lru_cache正确的是？","A. 必须指定maxsize  B. 使用LRU策略管理缓存  C. 不能用于递归函数  D. 只有@lru_cache装饰器","B","hard","lru_cache"),
    ("关于global关键字，以下正确的是？","A. 声明局部变量  B. 在函数中声明要修改的全局变量  C. Python关键字  D. 无关","B","medium","global"),
    ("itertools.count() 生成什么序列？","A. 有限序列  B. 无限递增整数序列  C. 斐波那契  D. 随机数","B","hard","itertools"),
    ("Python中作为装饰器的函数应当？","A. 返回None  B. 接收函数，返回包装后函数  C. 直接调用原函数  D. 修改原函数代码","B","medium","装饰器"),
    ("以下哪个是正则表达式中的量词？","A. .  B. *  C. ^  D. \\b","B","medium","正则量词"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

tf = [
    ("Python中，生成器使用惰性求值，节省内存。","true","easy","生成器"),
    ("lambda函数体内可以使用多条语句。","false","easy","lambda限制"),
    ("符合迭代器协议的对象支持__iter__()和__next__()方法。","true","medium","迭代器"),
    ("@装饰器的执行顺序是从下往上的。","false","medium","装饰器"),
    ("正则表达式\\w 匹配任意字母数字字符。","true","medium","正则"),
    ("functools.lru_cache可以用于任何函数。","false","hard","lru_cache"),
    ("闭包函数可以返回内部嵌套的函数对象。","true","hard","闭包"),
    ("re.search()和re.match()都在任意位置搜索模式。","false","medium","search vs match"),
    ("Python上下文管理器只能用于文件操作。","false","medium","上下文"),
    ("map(function, iterable) 返回一个map对象，需转换为列表才能用。","true","easy","map"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

fb = [
    ("以下代码的输出结果是：\ndef gen():\n    for x in range(3):\n        yield x\nprint(list(gen()))\n答：________","[0, 1, 2]","medium","生成器"),
    ("以下代码的输出结果是：\nnums = [1,2,3,4,5]\nprint(list(filter(lambda x: x>3, nums)))\n答：________","[4, 5]","medium","filter"),
    ("以下代码的输出结果是：\nfrom functools import reduce\nprint(reduce(lambda x,y: x+y, range(1,6)))\n答：________","15","medium","reduce"),
    ("以下代码的输出结果是：\nprint([x for x in range(10) if x%2==0 and x>5])\n答：________","[6, 8]","medium","列表推导式"),
    ("以下代码的输出结果是：\nimport re\nprint(len(re.findall(r'\\\d+', 'a12b34c')))\n答：________","2","medium","正则提取"),
    ("以下代码的输出结果是：\nfrom collections import Counter\nc = Counter('hellohello')\nprint(c.most_common(1)[0][0])\n答：________","l","medium","Counter"),
    ("以下代码的输出结果是：\nsq = [x**2 for x in range(5)]\nprint(sq[4])\n答：________","16","easy","列表推导式"),
    ("以下代码的输出结果是：\nclass CM:\n    def __enter__(self): return 'OK'\n    def __exit__(self,*a): pass\nwith CM() as x:\n    print(x)\n答：________","OK","hard","上下文管理器"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

cr = [
    ("阅读以下代码，输出结果是什么？\n\nimport functools\n@functools.lru_cache(maxsize=None)\ndef fib(n):\n    if n < 2: return n\n    return fib(n-1) + fib(n-2)\nprint(fib(5))","A. 3  B. 5  C. 8  D. 13","B","hard","lru_cache递归"),
    ("阅读以下代码，输出结果是什么？\n\ndef make_multiplier(n):\n    def multiply(x):\n        return x * n\n    return multiply\n\ndouble = make_multiplier(2)\ntriple = make_multiplier(3)\nprint(double(5), triple(5))","A. 7 8  B. 10 15  C. 5 5  D. 25 125","B","medium","闭包"),
    ("阅读以下代码，输出结果是什么？\n\nimport re\ntext = 'a1b2c3d4'\nmatches = re.findall(r'[a-z](\\\d)', text)\nprint(matches)","A. ['a','b','c','d']  B. ['1','2','3','4']  C. ['a1','b2','c3','d4']  D. ['1','2','3']","B","hard","正则分组"),
    ("阅读以下代码，输出结果是什么？\n\nm = [[1,2,3],[4,5,6],[7,8,9]]\nr = [x for row in m for x in row if x%2==0]\nprint(r)","A. [2,4,6,8]  B. [[2],[4,6],[8]]  C. [2,4,6]  D. [2,4,6,8]","A","hard","嵌套列表推导"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

sa = [
    ("请简述迭代器和迭代器对象(iterator)的区别，及如何创建一个迭代器类。","可迭代对象：实现了__iter__()方法，返回一个迭代器对象。迭代器对象(iterator)：实现了__iter__()和__next__()方法，逐步产生值。创建自定义迭代器类需同时实现__iter__()返回self，和__next__()方法返回下一个值或触发StopIteration。常见可迭代对象：list, tuple, dict, set, str。迭代器是一对一关系，通常只能遍历一次。","medium","迭代器"),
    ("请简述闭包(Closure)的概念及应用场景。","闭包定义：内部函数引用了外部函数的变量，并且内部函数作为外部函数的返回值。闭包能记住它创建时所在的环境（外部作用域中的变量）。特性：外部函数结束时，内部函数仍保持对外部变量的引用，不会释放。应用场景：延迟计算、工厂函数、回调函数、数据封装、模拟私有变量。","hard","闭包"),
    ("请简述装饰器(Decorator)的工作原理和常用的应用场景。","装饰器本质是一个接收函数对象并返回新函数对象（包装器）的函数。过程：@dec 等价于 func = dec(func)，即原函数替换为装饰后的包装器。包装器接收*args, **kwargs并在调用原函数前后执行附加操作。@functools.wraps保留元信息。应用场景：计时统计、日志记录、权限验证、结果缓存(@lru_cache)、异常重试、输入验证。","medium","装饰器"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

pr = [
    ("编写函数 retry(n)，返回一个装饰器，使被装饰函数在产生异常时自动重试最多n次。如果n次都失败，抛出最后一次的异常。","import functools\ndef retry(n):\n    def decorator(func):\n        @functools.wraps(func)\n        def wrapper(*args, **kwargs):\n            last_err = None\n            for _ in range(n):\n                try:\n                    return func(*args, **kwargs)\n                except Exception as e:\n                    last_err = e\n            raise last_err\n        return wrapper\n    return decorator","hard","装饰器"),
    ("编写Python生成器函数 primes(limit)，按顺序生成不大于limit的所有素数。","def primes(limit):\n    for n in range(2, limit+1):\n        is_prime = True\n        for i in range(2, int(n**0.5)+1):\n            if n % i == 0:\n                is_prime = False\n                break\n        if is_prime:\n            yield n","medium","生成器素数"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ==========================================================
# Exam 6: Web开发基础测试 (57题)
# ==========================================================
e = 6

sc = [
    ("Flask中用于定义路由的装饰器是？","A. @route  B. @app.route  C. @url  D. @path","B","easy","Flask路由"),
    ("Flask默认使用的模板引擎是？","A. Django Template  B. Jinja2  C. Mako  D. Mustache","B","easy","Jinja2"),
    ("Flask获取POST表单数据的属性是？","A. request.form  B. request.data  C. request.json  D. request.args","A","easy","表单"),
    ("SQLAlchemy中用于定义模型基类的是？","A. Base  B. Model  C. db.Model  D. SQLBase","C","easy","模型"),
    ("RESTful中GET方法的语义是？","A. 创建资源  B. 获取资源  C. 更新资源  D. 删除资源","B","easy","RESTful"),
    ("以下哪个动态路由可以只接收整数？","A. /user/<name>  B. /post/<int:id>  C. /page/<num>  D. /item/<str:code>","B","easy","路由类型"),
    ("Jinja2中输出变量的语法是？","A. <% var %>  B. {{ var }}  C. ${ var }  D. #{ var }","B","easy","模板变量"),
    ("Flask中设置secret_key的主要用途是？","A. 加密路由  B. 会话加密/签名  C. 压缩数据  D. 配置日志","B","medium","secret_key"),
    ("以下哪个SQLAlchemy方法用于添加记录？","A. db.add()  B. db.session.add()  C. db.insert()  D. db.create()","B","easy","添加记录"),
    ("Jinja2模板继承语法是？","A. {include}  B. {use}  C. {% extends %}  D. {inherit}","C","easy","模板继承"),
    ("Flask request.args 主要用于获取？","A. 表单数据  B. JSON数据  C. URL查询参数  D. Cookie","C","medium","request.args"),
    ("以下关于REST API正确的是？","A. 使用动词组成URL  B. 代表资源用名词，GET用于获取  C. POST请求无body  D. 不允许使用URL参数","B","medium","REST规范"),
    ("处理上传文件应使用哪个函数清理文件名？","A. safe_filename()  B. secure_filename()  C. clean_filename()  D. valid_filename()","B","easy","文件安全"),
    ("Flask的session数据默认存储于？","A. 服务器数据库  B. 客户端cookie(已签名)  C. 文件  D. 内存","B","medium","session"),
    ("以下关于SQLAlchemy filter_by()方法正确的是？","A. 可接受复杂条件  B. 简化精确字段比较(key=value)  C. 不支持整数参数  D. 不返回结果","B","medium","filter_by"),
    ("返回JSON响应在Flask中推荐使用？","A. json.dumps()  B. jsonify()  C. render()  D. response()","B","easy","jsonify"),
    ("以下哪条Jinja2注释是模板注释（不在HTML中渲染）？","A. <!-- comment -->  B. {# comment #}  C. /* comment */  D. // comment","B","medium","模板注释"),
    ("Flask中定义404错误页面使用？","A. @app.error(404)  B. @app.errorhandler(404)  C. @app.handle(404)  D. @app.route('/404')","B","hard","错误处理"),
    ("User.query.order_by(User.name.desc()).first() 返回什么？","A. 所有用户  B. 按姓名降序排列的第一个  C. 随机  D. 格式错误","B","medium","查询排序"),
    ("dict(form.data) 在Flask-WTF中指的是？","A. 表单中数据字典  B. 对象  C. 装饰器  D. html","A","medium","表单数据"),
    ("Flask中app = Flask(__name__)参数__name__的作用是？","A. 模块路径，帮助定位资源和配置  B. 随机名  C. 环境变量  D. 固定标识","A","easy","__name__"),
    ("Jinja2中{% for item in items %}...{% endfor %} 是什么？","A. 变量  B. 语句/控制结构  C. 注释  D. 过滤器","B","easy","控制结构"),
    ("关于数据库关系backref正确的是？","A. 定义了数据库存储结构  B. 在关系的另一侧自动创建反向引用属性  C. 不常用  D. 手动调用backref()","B","hard","backref"),
    ("用Flask渲染页面返回HTML的函数是？","A. render_template()  B. render_html()  C. response()  D. to_html()","A","easy","render_template"),
    ("db.session.commit() 的作用是？","A. 回滚  B. 提交事务持久化  C. 查询  D. 删除","B","easy","commit"),
    ("Jinja2/管道过滤器用法正确的是？","A. {{ name }}  B. {{ name | upper }}  C. {{ | upper }}  D. {{ upper:name }}","B","medium","过滤器"),
    ("db.Column(db.Integer, db.ForeignKey('user.id')) 的作用是？","A. 添加索引  B. 定义外键关联  C. 删除列  D. 忽略","B","medium","ForeignKey"),
    ("app.run(debug=True) 的主要功能？","A. 启动生产模式  B. 启用调试模式+自动重载  C. 跳过路由  D. 配置数据库","B","easy","debug"),
    ("User.query.get(1) 返回什么？","A. id为1的User对象或None  B. 所有用户  C. 异常  D. 字典","A","medium","get方法"),
    ("restful: /api/users/123 获得id=123信息，应使用HTTP方法____? ","A. POST  B. GET  C. DELETE  D. PUT","B","medium","RESTful"),
]
for i, (text, opts, ans, diff, kp) in enumerate(sc, 1):
    add_q(e, 'single_choice', text, opts, ans, 1.5, i, diff, kp)

tf = [
    ("Flask应用config对象对JSON数据无需设置。","false","easy","配置"),
    ("Flask实现RESTful API可以使用jsonify()返回数据。","true","easy","jsonify"),
    ("SQLAlchemy查询会自动关闭连接。","true","medium","连接管理"),
    ("Flask request.form可以获取查询参数。","false","easy","form"),
    ("Jinja2支持模板继承。","true","easy","继承"),
    ("Flask的路由必须指定methods=['GET']。","false","medium","路由方法"),
    ("db.relationship用于定义外键列。","false","hard","relationship"),
    ("Flask session在访问前不需要设置secret_key。","false","medium","session"),
    ("RESTful API可以定义不同的HTTP方法来操作同一资源。","true","easy","RESTful"),
    ("Flask中的@app.before_request装饰器可以在请求前运行函数。","true","hard","钩子"),
]
for i, (text, ans, diff, kp) in enumerate(tf, 31):
    add_q(e, 'true_false', text, '', ans, 1.0, i, diff, kp)

fb = [
    ("Flask中获取当前请求的方法，使用request.________。","method","medium","请求方法"),
    ("SQLAlchemy声明模型继承自________。","db.Model","easy","模型"),
    ("Flask中发送JSON响应常用的函数是________。","jsonify()","easy","JSON响应"),
    ("以下代码中SecretKey用途是________。\nfrom flask import Flask, session\napp = Flask(__name__)\napp.secret_key = 'my-key'\n答：________","加密session会话","medium","secret_key"),
    ("以下代码查询所有用户正确的OR语句方式\nUser.query.filter(db.or_(User.name.like(...),...)).________","all()","medium","复杂查询"),
    ("以下查询中，peewee写法等效于SQLAlchemy db.session.add(record);________","commit()","medium","事务"),
    ("Flask中动态路由参数使用尖括号定义类型如<int:id>；读取时直接使用函数的同名________。","参数","easy","路由参数"),
    ("以下代码的输出结果是：\nfrom flask import Flask, jsonify\napp = Flask(__name__)\nwith app.test_request_context('/api/data'):\n    resp = jsonify({'status':'ok'})\n    print(resp.json)\n答：________","{'status': 'ok'}","hard","context"),
]
for i, (text, ans, diff, kp) in enumerate(fb, 41):
    add_q(e, 'fill_blank', text, '', ans, 1.5, i, diff, kp)

cr = [
    ("阅读以下代码，选项正确的是？\n\nclass User(db.Model):\n    id = db.Column(db.Integer,primary_key=True)\n    name = db.Column(db.String(80))\n    posts = db.relationship('Post',backref='author')\n\nclass Post(db.Model):\n    id = db.Column(db.Integer,primary_key=True)\n    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))","A. Post有author属性  B. User没有posts属性  C. 无法反向查询  D. 错误","A","hard","relationship"),
    ("阅读以下代码，输出结果是什么？\n\ndef decorator(func):\n    def wrapper(*a,**kw):\n        result = func(*a,**kw)\n        return f'[<b>{result}</b>]'\n    return wrapper\n\n@app.route('/greet/<name>')\n@decorator\ndef greet(name):\n    return f'Hello {name}'\n\n访问 /greet/John , 浏览器页面内容可能是什么？","A. Hello John  B. [<b>Hello John</b>]  C. 错误  D. 空","B","hard","装饰器Web"),
    ("阅读以下模板代码，输出结果是什么？\n\n{% set x = 10 %}\n{% if x > 5 %}\n    Big\n{% else %}\n    Small\n{% endif %}","A. Big  B. Small  C. 10  D. Error","A","medium","模板条件"),
    ("阅读以下代码并指出不符合RESTful的问题：\n@app.route('/delete_user/<id>')\ndef del_user(id):\n    User.query.filter_by(id=id).delete()\n    db.session.commit()\n    return 'Deleted'","A. URL使用动词delete_user  B. 方法未限定DELETE方法  C. 返回状态码不清楚  D. 以上所有","D","medium","RESTful规范"),
]
for i, (text, opts, ans, diff, kp) in enumerate(cr, 49):
    add_q(e, 'code_reading', text, opts, ans, 3.0, i, diff, kp)

sa = [
    ("请简述Flask中请求-响应生命周期（Request-Response Lifecycle）的主要阶段。","1.用户发送HTTP请求到服务器，WSGI接收；2.Flask创建request上下文（线程局部）包含请求信息；3.URL路由匹配规则，找到视图函数或errorhandler（404等）；4.执行before_request注册的装饰器函数；5.执行视图函数，处理逻辑生成响应；6.执行after_request注册函数（拦截响应）；7.返回HTTP响应给客户端；8.上下文清理及teardown调用。","medium","生命周期"),
    ("请简述SQLAlchemy中ORM操作的基本模式：定义模型、查询和CRUD的关键方法。","定义模型：通过db.Model继承，类属性定义db.Column(类型, 约束, 主键, 外键等)。查询：Model.query 获取查询对象，filter/filter_by 过滤，all()返回列表、first()返回单个对象或None，get(id)按主键查询。创建：obj = Model(field=value)；db.session.add(obj)；更新：obj.field = new_val；db.session.commit()；删除：db.session.delete(obj) 或 对象操作方法（.delete()）。保存都需commit事务。","medium","ORM CRUD"),
    ("请简述RESTful API规范中资源定位与HTTP方法的设计原则及正确状态码使用。","URL设计原则：资源名词复数复数（如GET /users/）定位集合，/users/{id} 定位单个资源，避免使用动词。HTTP方法语义：GET 获取（幂等）、POST 新建、PUT/PATCH 修改（幂等）、DELETE 删除（幂等）。状态码：200 OK(GET/PUT)、201 Created(POST)、204 No Content(DELETE)、400 Bad Request(参数错误)、401 Unauthorized(未认证)、403 Forbidden(权限)、404 Not Found、500 Server Error。","medium","RESTful规范"),
]
for i, (text, ans, diff, kp) in enumerate(sa, 53):
    add_q(e, 'short_answer', text, '', ans, 3.0, i, diff, kp)

pr = [
    ("编写一个Flask视图函数 (app.py) 来实现用户创建注册API。接收POST JSON `{username:'test', password:'123'}`，检查密码长度至少6位，用户名长度≥3，返回创建结果。状态码：201成功，400输入无效。","from flask import Flask, request, jsonify\napp = Flask(__name__)\n@app.route('/api/users', methods=['POST'])\ndef create_user():\n    data = request.get_json()\n    if not data or 'username' not in data or 'password' not in data:\n        return jsonify({'error':'Invalid data'}), 400\n    username = data['username']\n    password = data['password']\n    if len(username.strip()) < 3:\n        return jsonify({'error':'Username >= 3 chars'}), 400\n    if len(password) < 6:\n        return jsonify({'error':'Password >= 6 chars'}), 400\n    # Here normally call db.create or model\n    return jsonify({'id':1, 'username':username}), 201","medium","注册API"),
    ("编写SQLAlchemy模型`Post`，字段：id (主键,Integer)、title (字符串,200) 、content (文本Text)、user_id (外键关联User模型) 和 author (relationship反向引用'posts')。并完成添加新文章方法(假设`request.form`已有title,content,user_id)。注意不一定存在User。","from flask import request\nfrom flask_sqlalchemy import SQLAlchemy\ndb = SQLAlchemy()\nclass Post(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    title = db.Column(db.String(200), nullable=False)\n    content = db.Column(db.Text)\n    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))\n    author = db.relationship('User', backref='posts')\n\ndef add_post(): \n    title = request.form.get('title')\n    content = request.form.get('content')\n    uid = request.form.get('user_id', type=int)\n    if title:\n        post = Post(title=title, content=content, user_id=uid)\n        db.session.add(post)\n        db.session.commit()\n        return post.id\n    return None","hard","模型创建"),
]
for i, (text, ans, diff, kp) in enumerate(pr, 56):
    add_q(e, 'programming', text, '', ans, 6.0, i, diff, kp)

# ============== Serialize to text ==================
def format_question(q):
    """Format a question dict as a Python dict literal for the file"""
    def esc(s):
        return s.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'").replace('\n', '\\n')
    opts = q['options']
    text_escaped = esc(q['text'])
    ans_escaped = esc(q['answer'])
    opts_escaped = esc(opts) if opts else ""
    kp = esc(q['knowledge_point'])
    
    return (
        f"    {{\"exam\":{q['exam']},\"type\":\"{q['type']}\",\"text\":\"{text_escaped}\","
        f"\"options\":\"{opts_escaped}\",\"answer\":\"{ans_escaped}\","
        f"\"points\":{q['points']},\"order\":{q['order']},"
        f"\"difficulty\":\"{q['difficulty']}\",\"knowledge_point\":\"{kp}\",\"lesson_id\":0}},"
    )

# Build EXAM_QUESTIONS section for exams 1-6
q_lines = []
q_lines.append("EXAM_QUESTIONS = [")
for q in new_questions:
    q_lines.append(format_question(q))
q_lines.append("")

# Now find Exam 7 section in the original
exam7 = content[exam7_pos:]

# Combine: pre + EXAM_QUESTIONS with new q + Exam7
output = pre_content + "\n".join(q_lines) + "\n" + exam7

# Write
with open('course_data.py', 'w', encoding='utf-8') as f:
    f.write(output)

print(f"Total new questions generated: {len(new_questions)}")
print("course_data.py updated successfully!")
