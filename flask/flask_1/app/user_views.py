import random

from flask import render_template, Blueprint, request, make_response, redirect, \
    url_for, session

# 导入蓝本 main_blueprint
from app.models import db, Student, User, Grade

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/')
def index():
    return render_template('index.html')


@user_blueprint.route('/setcookie/')
def set_cookie():
    """
    设置cookie
    """
    temp = render_template('cookies.html')
    # 服务端创建相应
    res = make_response(temp)
    # 绑定cookie值, set_cookie(key, value, max_age, expries)
    res.set_cookie('ticket', '123123', max_age=10)
    return res


@user_blueprint.route('/delcookie/')
def del_cookie():
    """
    设置cookie
    """
    temp = render_template('cookies.html')
    # 服务端创建相应
    res = make_response(temp)
    # 删除cookie值
    res.delete_cookie('ticket')
    return res


@user_blueprint.route('/scores/', methods=['GET'])
def stu_scores():
    scores = [1, 2, 3, 4, 5]
    content_h2 = '<h2>哈哈哈</h2>'
    content_h3 = ' <h3>哈哈哈</h3> '
    return render_template('score.html', scores=scores, content_h2=content_h2, content_h3=content_h3)


@user_blueprint.route('/create_db/')
def create_db():
    # 创建数据表
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    # 删除数据表
    db.drop_all()
    return '删除成功'


@user_blueprint.route('/add_grades/')
def add_grades():
    grade_list = []
    grades = {
        'python': '人生苦短, Python当歌',
        'GO': 'go_go_go_',
        'php': '全世界最好的语言',
        'java': '暂无',
        'UI': '暂无',
        'html': '暂无'
    }

    for key, value in grades.items():
        grade = Grade()
        grade.g_name = key
        grade.g_desc = value
        grade_list.append(grade)

    db.session.add_all(grade_list)
    db.session.commit()
    return '添加班级成功'


@user_blueprint.route('/grade_list/')
def grade_list():
    grades = Grade.query.all()
    return render_template('grade.html', grades=grades)


@user_blueprint.route('/create_user_by_grade/', methods=['GET', 'POST'])
def create_user_by_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        grade = Grade.query.get(g_id)
        return render_template('stu_edit.html', grade=grade, stu=None)
    if request.method == 'POST':
        g_id = request.args.get('g_id')
        s_name = request.form.get('username')
        stu = Student(s_name, g_id)
        db.session.add(stu)
        db.session.commit()
    return redirect(url_for('user.grade_list'))


@user_blueprint.route('/select_stu_by_grade/', methods=['GET'])
def select_stu_by_grade():
    if request.method == 'GET':
        g_id = request.args.get('g_id')
        g = Grade.query.get(g_id)
        stus = g.students
        return render_template('students.html', stus=stus)


@user_blueprint.route('/create_stu/', methods=['GET', 'POST'])
def create_stu():
    if request.method == 'GET':
        return render_template('stu_edit.html', stu=None, grade=None)
    if request.method == 'POST':
        s_name = request.form.get('username')
        g_name = request.form.get('g_name')
        grade_id = Grade.query.get(g_name).first().g_id
        stu = Student(s_name, grade_id)
        db.session.add(stu)
        db.session.commit()
    return redirect(url_for('user.stu_list'))


@user_blueprint.route('/create_stus/', methods=['GET'])
def create_stus():
    stu_list = []
    for i in range(10):
        # 第一种
        # stu = Student()
        # stu.s_name = '张三%s' % i
        # stu.s_age = '%s' % random.randrange(20)

        # 第二种
        stu = Student('张思%s' % i, '%d' % random.randrange(6))
        stu_list.append(stu)

    # 创建数据
    db.session.add_all(stu_list)
    db.session.commit()
    return '添加许多学生成功'


@user_blueprint.route('/stu_list/', methods=['GET'])
def stu_list():
    # 查找
    # stus = Student.query.filter(Student.s_name == '张三')
    stus = Student.query.all()
    # stu = Student.query.filter_by(s_name='张三')
    #
    # sql = 'select * from tb_student'
    # stus = db.session.execute(sql)
    # in_ 在范围内
    # stus = Student.query.filter(Student.s_id.in_([2, 3, 4, 5, 6]))
    # stus = Student.query.filter(Student.s_age.endswith('9'))
    # stus = Student.query.filter(Student.s_age.contains('1'))
    # stus = Student.query.filter(Student.s_age.__le__('19'))
    # 获取前五个
    # stus = Student.query.limit(5)
    # 跳过前三个
    # stus = Student.query.order_by('s_id').offset(3).limit(5)
    # 分页
    # stus = Student.query.paginate(1, 5, False)
    return render_template('students.html', stus=stus)


@user_blueprint.route('/paging/', methods=['GET'])
def stu_paging():
    """分页"""
    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        page_num = 5
        paginate = Student.query.order_by('s_id').paginate(page, page_num)
        stus = paginate.items
        return render_template('stu_paginate.html', stus=stus, paginate=paginate)


@user_blueprint.route('/update_stu/', methods=['GET', 'POST'])
def update_stu():
    # 更新
    if request.method == 'GET':
        s_id = request.args.get('s_id')
        stu = Student.query.filter_by(s_id=s_id).first()
        g_id = request.args.get('g_id')
        grade = Grade.query.get(g_id)
        return render_template('stu_edit.html', stu=stu, grade=grade)
    if request.method == 'POST':
        s_id = request.form.get('s_id')
        s_name = request.form.get('username')
        g_name = request.form.get('g_name')
        grade_id = Grade.query.filter_by(g_name=g_name).first().g_id
        stu = Student.query.filter_by(s_id=s_id).first()
        stu.s_name = s_name
        stu.grade_id = grade_id
        db.session.commit()
    return redirect(url_for('user.stu_list'))


@user_blueprint.route('/del_stu/', methods=['GET'])
def del_stu():
    # 删除
    if request.method == 'GET':
        id = request.args.get('id')
        stu = Student.query.filter_by(s_id=id).first()
        db.session.delete(stu)
        db.session.commit()
    return redirect(url_for('user.stu_list'))


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter(User.username == username).first()
        if not user:
            msg = '用户不存在'
            return render_template('login.html', msg=msg)
        if user.password == password:
            session['uid'] = user.u_id
            return redirect(url_for('user.index'))
        else:
            msg = '用户名或密码错误'
            return render_template('login.html', msg=msg)


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        if password != password1:
            msg = '两次密码不一致'
            return render_template('register.html', msg=msg)
        user = User()
        user.username = username
        user.password = password
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('user.login'))
