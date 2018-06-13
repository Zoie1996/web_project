### 1. 最小项目

```python
文件名:hello.py

from flask import Flask
app = Flask(__name__)
@app.route('/')
def hello():
	return 'hello world'

if __name__ == '__main__':
	app.run()

# 启动项目
$ python hello.py

# 修改启动方式
app.run(debug=True, port=8080, host='0.0.0.0')

# 修改启动方式
$ pip install flask_script

from flask_script import Manager
manege = Manager(app=app)
# 启动命令
$ python hello.py runserver -h 0.0.0.0 -p 8080 -d
```

### 2. Session / Cookie

- **Cookie**

Cookie是通过服务器创建的Response来创建的
设置：set_cookie('key', value, max_ages='')
删除：del_cookie('key')

```
@main.route('/setcookie/')
def set_cookie():
    temp = render_template('index.html')
    response = make_response(temp)
    response.set_cookie('name','cocoococo')
    return response
```

- **Session**

flask-session是flask框架的session组件

**安装: **

```
pip install flask-session
```

如果指定存session的类型为redis的话，需要安装redis 

```
pip install redis
```

**配置session**  utlis/functions.py

```python
def create_app():
    app = Flask(__name__)
    # SECRET_KEY 秘钥
    app.config['SECRET_KEY'] = 'secret_key'
	# session类型为redis
    app.config['SESSION_TYPE'] = 'redis'
	# 添加前缀
	app.config['SESSION_KEY_PREFIX'] = 'flask'
    
    # 加载app的第一种方式
    se = Session()
    se.init_app(app=app)
    #加载app的第二种方式
    Session(app=app)
    app.register_blueprint(blueprint=blue)

    return app
```

### 3.  项目目录

```python
|__ Project_name
	|__ app
		|__ __init__.py
		|__ models.py
		|__ views.py
	|__ static
		|__ css.css
		|__ js.js
	|__ templates
		|__ html.html
	|__ utils
		|__ __init__.py
		|__ functions.py
	|__ manage.py
```

app/views.py 视图文件

```python
from flask import Blueprint

main = Blueprint('hello', __name__)

@main.route('/')
def index():
    return 'hello'
```

utils/functions.py 公共文件

```python
from flask import Flask
from app.views import main

def create_app():
    # 实例化app
    app = Flask(__name__)
    # 注册app
    app.register_blueprint(blueprint=hello, url_prefix='/main')
    return app
```

manage.py 管理文件

```python
from flask_script import Manager
from utils.functions import create_app

app = create_app()
# 修改启动方式
manager = Manager(app=app)

if __name__ == '__main__':
    # 启动项目
    manager.run()
```

Configuretion 配置

```pyhton
Parameter runserver -p 5000 -d
```

### 4. Flask模板

#### 1.模板语法

- 变量和标签

  变量: {{ var }}

  标签: {% tag %}

- 结构标签

   **块** 

   定义模板  templates/base.html 

    ```html
   <!DOCTYPE html>
   <html lang="en">
   <head>
       <meta charset="UTF-8">
       <title>
           {% block title %}
           {% endblock %}
       </title>
   {% block extCSS %}
   {% endblock %}
   </head>
   <body>
   {% block content %}
   {% endblock %}
   {% block footer %}
   {% endblock %}
   
   {% block extJS  %}
   {% endblock %}
   </body>
   </html>
    ```

   定义基础模板  templates/base_main.html 

   ```
   {% extends 'base.html' %}
   
   {% block extCSS %}
       <link rel="stylesheet" href="{{ url_for('static', filename='css/main.css') }}">
   {% endblock %}
   ```

   **继承**

   ```html
   {% extends ‘base.html’ %}
   <!-- 继承以后保留块中的内容 -->
   {% super() %}
   ```

   **函数**

   templates/common.html

   ```html
   {% macro create_user(name) %}
       创建了一个用户:{{ name }}
   {% endmacro %}
   ```

   templates/index.html

   ```html
   {% from 'functions.html' import create_user %}
   
   {{ create_user('小花') }}
   ```

   **循环**

   ```html
   {% for item in cols %}
   	aa
   {% else %}
   	bb
   {% endfor %}
   <!-- 获取循环信息循环 -->
   loop.first
   loop.last
   loop.index
   loop.revindex
   ```

   **过滤器**

   ```html
   {{ 变量|过滤器|过滤器... }}
   capitalize 单词首字母大写
   lower 单词变为小写
   upper 单词变为大写
   title
   trim 去掉字符串的前后的空格
   reverse 单词反转
   format
   striptags 渲染之前，将值中标签去掉
   safe 讲样式渲染到页面中
   default
   last 最后一个字母
   first
   length
   sum
   sor
   ```


### 5. 数据库

定义模型  app/models.py 

```python
from flask_sqlalchemy import SQLAlchemy

# 实例化
db = SQLAlchemy()

class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(10), unique=True)
    s_age = db.Column(db.Integer, default=18)
    grade_id = db.Column(db.Integer, db.ForeignKey('grade.g_id'), nullable=True)
    # 设置数据库名称
    __tablename__ = 'tb_student'
    
class Grade(db.Model):
    g_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    g_name = db.Column(db.String(10), unique=True)
    g_desc = db.Column(db.String(100), nullable=True)
    g_time = db.Column(db.Date, default=datetime.now)
    # 外键 ForeignKey('多_表名.字段')
    # backref 多表反查时的名称
    students = db.relationship('Student', backref='grade', lazy=True)

    __tablename__ = 'grade'
```

初始化SQLALchemy  utils/functions.py

```python
from app.models import db
from flask_sqlalchemy import SQLALchemy
# 初始化数据库文件, 配置数据库访问地址
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flask"
app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False
# 第一种
db = SQLAlchemy(app)
# 第二种
db.init_app(app=app)
```

数据库增删改查 app/views.py

```python
from app.models import db
# 创建数据表
def create_db():
    # 创建表
    db.create_all()
    return '创建表成功'

# 删除数据表
def drop_db():
    # 删除表
    db.drop_all()
    return '删除表成功'

# 添加一条数据
def create_stu():
    # 添加
    stu = Student()
    stu.s_name = '张三'
    stu.s_age = '17'
    db.session.add(stu)
    db.session.commit()
    return '添加数据成功'

# 添加多条数据
def create_stus():
    stu_list = []
    for i in range(10):
        # 第一种
        stu = Student()
        stu.s_name = '张三%s' % i
        stu.s_age = '%s' % random.randrange(20)

        # 第二种
        stu = Student('张思%s' % i,'%s' % random.randrange(20))
        stu_list.append(stu)
        
    db.session.add_all(stu_list)
    db.session.commit()
    return '添加多条数据成功'


# 查询数据
def select_stu():
    # stus = Student.query.filter(Student.s_name == '张三')
    stus = Student.query.all()
    # stus = Student.query.filter_by(s_name='张三')
    # stu = Student.query.get(5)
    # 使用原生SQL查询
    sql = 'select * from tb_student'
    stus = db.session.execute(sql)
    return render_template('students.html', stus=stus)

# 更新数据
def update_stu():
    stu = Student.query.filter_by(s_name='张思').first()
    stu.s_name = '张四'
    db.session.add(stu)
    db.session.commit()
    return render_template('students.html')

# 删除数据
def del_stu():
    stu = Student.query.filter_by(s_name='张四').first()
    db.session.delete(stu)
    db.session.commit()
    return render_template('students.html')
```

注意：

- **filter**  <flask_sqlalchemy.BaseQuery object at 0x10f2f0ba8>

- **filter_by**   <flask_sqlalchemy.BaseQuery object at 0x10f2f0ba8>
- **filter / filter_by.first()** 返回单个结果
- **get**  <==> **filter / filter_by.first()**  没有结果返回空 (Django get没有结果会报错)
- **all** 结果是一个list的结果集

**重点注意：在增删改中如果不commit的话，数据库中的数据并不会更新，只会修改本地缓存中的数据，所以一定需要db.session.commit()**

**运算符**

```python
contains： 包含
startswith：以什么开始
endswith：以什么结束
in_：在范围内
like：模糊
__gt__: 大于
__ge__：大于等于
__lt__：小于
__le__：小于等于
# 例子
stus = Student.query.filter(Student.s_id.in_([2, 3, 4, 5, 6]))
stus = Student.query.filter(Student.s_age.endswith('9'))
stus = Student.query.filter(Student.s_age.contains('1'))
```

**逻辑运算**

```python
与 and_
filter(and_(条件[,条件…])
或 or_
filter(or_(条件[,条件…])
非 not_
filter(not_(条件[,条件…])
# 列子
students = Student.query.filter（and_（Student.s_age == 18，Student.s_name =='雅典娜'））
students = Student.query.filter（or_（Student.s_age == 18，Student.s_name =='雅典娜'））
students = Student.query.filter（not_（Student.s_age == 18））
```

**筛选**

```python
limit() 截取
offset() 跳过
order_by() 排序
paginate() 分页
# 例子
# 获取前五个
stus = Student.query.limit(5)
# 跳过前三个
stus = Student.query.order_by('s_id').offset(3).limit(5)
```

**分页**

```pyhton
items     当前页面中的记录
query     分页的源查询
page      当前页数
prev_num  上一页的页数
next_num  下一页的页数
has_prev  如果有上一页, 返回True
has_next  如果有下一页, 返回True
pages     查询得到的总页数
per_page  每页显示的记录数量
total     查询返回的记录总数
```











