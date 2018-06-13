from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# 实例化
db = SQLAlchemy()


class Student(db.Model):
    __tablename__ = 'tb_student'
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(10), unique=True)
    s_age = db.Column(db.Integer, default=18)
    # 外键 ForeignKey('多_表名.字段')
    grade_id = db.Column(db.Integer, db.ForeignKey('tb_grade.g_id'), nullable=True)

    # s_yuwen = db.Column(db.Float)
    # 设置数据库名称

    def __init__(self, s_name, grade_id):
        self.s_name = s_name
        self.grade_id = grade_id


class Grade(db.Model):
    __tablename__ = 'tb_grade'
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(16), unique=True, nullable=False)
    g_desc = db.Column(db.String(30), nullable=True)
    g_create_time = db.Column(db.DateTime, default=datetime.now)
    students = db.relationship('Student', backref='grade', lazy=True)


class User(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(30))

    __tablename__ = 'tb_user'
