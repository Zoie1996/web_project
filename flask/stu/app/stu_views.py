from flask import Blueprint, render_template, request, redirect, url_for

from app.models import Grade, Student, db
from utils.decoration import is_login

stu_blueprint = Blueprint('stu', __name__)


@stu_blueprint.route('/head/')
def head():
    return render_template('head.html')


@stu_blueprint.route('/left/')
def left():
    return render_template('left.html')


@stu_blueprint.route('/grades/')
# @is_login
def grades():
    grades = Grade.query.all()
    return render_template('grade.html', grades=grades)


@stu_blueprint.route('/grade_edit/<int:g_id>/', methods=['GET', 'POST'])
def grade_edit(g_id):
    if request.method == 'GET':
        grade = Grade.query.get(g_id)
        return render_template('addgrade.html', grade=grade)
    if request.method == 'POST':
        g_name = request.form.get('g_name')
        g_desc = request.form.get('g_desc')
        grade = Grade.query.get(g_id)
        grade.g_name = g_name
        grade.g_desc = g_desc
        grade.save()
        return redirect(url_for('stu.grades'))


@stu_blueprint.route('/add_grade/', methods=['GET', 'POST'])
def add_grade():
    """
    添加多个班级
    grades = {
        'python': '人生苦短, Python当歌',
        'GO': 'go_go_go_',
        'php': '全世界最好的语言',
        'java': '一个编程语言',
        'UI': '用户界面设计',
        'html': 'web语言'
    }
    for g_name, g_desc in grades.items():
        grade = Grade(g_name, g_desc)
        grade.save()
    return '添加班级成功'
    """
    if request.method == 'GET':
        return render_template('addgrade.html', grade=None)
    if request.method == 'POST':
        g_name = request.form.get('g_name')
        g_desc = request.form.get('g_desc')
        grade = Grade(g_name, g_desc)
        grade.save()
        return redirect(url_for('stu.grades'))


@stu_blueprint.route('/students/', methods=['GET', 'POST'])
@is_login
def students():
    if request.method == 'GET':
        students = Student.query.all()
        return render_template('student.html', students=students)


@stu_blueprint.route('/add_stu/', methods=['GET', 'POST'])
def add_stu():
    """
    添加多个班级
    for i in range(10):
        stu = Student('小%s' % i, '%d' % random.randrange(1,7))
        stu.save()
    return '添加许多学生成功'
    """
    if request.method == 'GET':
        grades = Grade.query.all()
        return render_template('addstu.html', grades=grades)
    if request.method == 'POST':
        s_name = request.form.get('s_name')
        g_id = request.form.get('g_id')
        stu = Student(s_name, g_id)
        stu.save()
        return redirect(url_for('stu.students'))


@stu_blueprint.route('/del_stu/<int:s_id>', methods=['GET'])
def del_stu(s_id):
    if request.method == 'GET':
        # Student.query.filter_by(s_id = s_id).delete()
        student = Student.query.get(s_id)
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('stu.students'))
