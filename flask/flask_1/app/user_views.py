import random
from flask import render_template, Blueprint, request, redirect, \
    url_for, session, jsonify
from flask_restful import Resource
from utils.decoration import is_login
from app.models import db, Student, User, Grade, Course
from utils.exts_init import api

user_blueprint = Blueprint('user', __name__)


class CourseApi(Resource):

    def get(self):
        courses = Course.query.all()
        return {
            'code': 200,
            'msg': '请求成功',
            'data': [course.to_dict() for course in courses]
        }

    def post(self):
        course_list = []
        courses = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']
        for c in courses:
            course = Course()
            course.c_name = c
            course_list.append(course)

        db.session.add_all(course_list)
        db.session.commit()
        return {
            'code': 200,
            'msg': '添加成功'
        }

    def put(self, id):
        pass

    def patch(self, id):
        course = Course.query.get(id)
        c_name = request.form.get('c_name')
        course.c_name = c_name
        course.save()
        return {
            'code': 200,
            'msg': '更新成功',
            'data': course.to_dict()
        }

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {
            'code': 200,
            'msg': '删除成功'
        }


api.add_resource(CourseApi, '/api/course/', '/api/course/<int:id>/')


@user_blueprint.route('/')
def index():
    return render_template('index.html')


@user_blueprint.route('/create_db/')
def create_db():
    # 创建数据表
    db.create_all()
    return '创建成功'


@user_blueprint.route('/drop_db/')
def drop_db():
    """删除数据表"""
    db.drop_all()
    return '删除成功'


@user_blueprint.route('/create_course/')
def create_course():
    """添加课程"""
    course_list = []
    courses = ['语文', '数学', '英语', '物理', '化学', '生物', '政治', '历史', '地理']
    for c in courses:
        course = Course()
        course.c_name = c
        course_list.append(course)

    db.session.add_all(course_list)
    db.session.commit()
    return '添加课程成功'


@user_blueprint.route('/add_grades/')
def add_grades():
    """
    添加班级
    """
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


@user_blueprint.route('/add_course/', methods=['GET', 'POST'])
def add_course():
    if request.method == 'GET':
        courses = Course.query.all()
        return render_template('course.html', courses=courses)
    if request.method == 'POST':
        s_id = request.args.get('s_id')
        c_id = request.form.get('course_id')
        stu = Student.query.get(s_id)
        course = Course.query.get(c_id)
        # 添加学生信息 course.students返回一个列表
        course.students.append(stu)
        db.session.add(course)
        db.session.commit()
        return redirect(url_for('user.grade_list'))


@user_blueprint.route('/show_course/<int:s_id>/', methods=['GET'])
def show_course(s_id):
    if request.method == 'GET':
        stu = Student.query.get(s_id)
        # 学生反查课程
        courses = stu.course
        return render_template('show_course.html', courses=courses, stu=stu)


@user_blueprint.route('/stu/<int:s_id>/del_course/<int:c_id>/', methods=['GET'])
def del_course(s_id, c_id):
    if request.method == 'GET':
        course = Course.query.get(c_id)
        stu = Student.query.get(s_id)
        course.students.remove(stu)
        db.session.commit()
        return redirect(url_for('user.grade_list'))


@user_blueprint.route('/grade_list/')
@is_login
def grade_list():
    """
    显示班级
    """
    grades = Grade.query.all()
    return render_template('grade.html', grades=grades)


@user_blueprint.route('/create_user_by_grade/', methods=['GET', 'POST'])
def create_user_by_grade():
    """
    通过班级列表创建学生
    """
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
    """
    通过班级列表显示学生列表
    """
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
    """
    删除学生
    """
    if request.method == 'GET':
        id = request.args.get('id')
        stu = Student.query.filter_by(s_id=id).first()
        db.session.delete(stu)
        db.session.commit()
    return redirect(url_for('user.stu_list'))


@user_blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    """
    登录
    """
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            msg = '请填写完整的登录信息'
            return render_template('login.html', msg=msg)

        user = User.query.filter(User.username == username).first()
        if user:
            if user.password == password:
                session['user_id'] = user.u_id
                return redirect(url_for('user.grade_list'))
            else:
                msg = '用户名或密码错误'
                return render_template('login.html', msg=msg)
        else:
            msg = '用户名错误'
            return render_template('login.html', msg=msg)


@user_blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """
    注册
    """
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password1 = request.form.get('password1')
        flag = True
        if not all([username, password, password1]):
            msg, flag = '请填写完整的注册信息', False
        if len(username) > 10:
            msg, flag = '用户名太长, 请重新输入', False
        if password != password1:
            msg, flag = '两次密码不一致', False
        if not flag:
            return render_template('register.html', msg=msg)
        user = User(username, password)
        user.save()
        return redirect(url_for('user.login'))
