from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# 实例化
db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'tb_student'
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(10), unique=True)
    s_age = db.Column(db.Integer, default=18)
    # 外键 ForeignKey('一_表名.字段')
    grade_id = db.Column(db.Integer, db.ForeignKey('tb_grade.g_id'), nullable=True)

    # 设置数据库名称

    def __init__(self, s_name, grade_id):
        self.s_name = s_name
        self.grade_id = grade_id

    def to_dict(self):
        return {
            's_id': self.s_id,
            's_name': self.s_name,

        }


class Grade(db.Model):
    __tablename__ = 'tb_grade'
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(16), unique=True, nullable=False)
    g_desc = db.Column(db.String(30), nullable=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    # 第一个参数关联模型名称  lazy=True 访问时则加载全部数据
    students = db.relationship('Student', backref='grade', lazy=True)


sc = db.Table('sc',
              db.Column('s_id', db.Integer, db.ForeignKey('tb_student.s_id'), primary_key=True),
              db.Column('c_id', db.Integer, db.ForeignKey('tb_course.c_id'), primary_key=True),
              )


class Course(db.Model):
    """
    学生表 课程表
    多    多

    """
    __tablename__ = 'tb_course'
    c_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    c_name = db.Column(db.String(16), unique=True)
    c_create_time = db.Column(db.DateTime, default=datetime.now)
    # 关联模型名称 中间表名称 反查名称
    students = db.relationship('Student', secondary=sc, backref='course')

    def to_dict(self):
        return {
            'c_id': self.c_id,
            'c_name': self.c_name,
            'c_create_time': self.c_create_time.strftime('%Y-%m-%d'),
            'students': [student.to_dict() for student in self.students]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(30))

    __tablename__ = 'tb_user'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
