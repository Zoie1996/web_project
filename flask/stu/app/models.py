from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

# 实例化
db = SQLAlchemy()


class Student(db.Model):
    s_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    s_name = db.Column(db.String(10), unique=True)
    grade_id = db.Column(db.Integer, db.ForeignKey('tb_grade.g_id'), nullable=True)

    # 设置数据库名称
    __tablename__ = 'tb_student'

    def __init__(self, s_name, grade_id):
        self.s_name = s_name
        self.grade_id = grade_id

    def save(self):
        db.session.add(self)
        db.session.commit()


class Grade(db.Model):
    """
    创建班级模型
    """
    g_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    g_name = db.Column(db.String(10), unique=True)
    g_desc = db.Column(db.String(100), nullable=True)
    students = db.relationship('Student', backref='grade', lazy=True)

    __tablename__ = 'tb_grade'

    def __init__(self, g_name, g_desc):
        self.g_name = g_name
        self.g_desc = g_desc

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):
    u_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(10))
    password = db.Column(db.String(30))
    role = db.relationship('Role', backref='user', uselist=False)

    __tablename__ = 'tb_user'

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Permission(db.Model):
    p_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    p_name = db.Column(db.String(10))
    p_en = db.Column(db.String(16))
    __tablename__ = 'tb_permission'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


r_p = db.Table('tb_r_p',
               db.Column('p_id', db.Integer, db.ForeignKey('tb_permission.p_id'), primary_key=True),
               db.Column('r_id', db.Integer, db.ForeignKey('tb_role.r_id'), primary_key=True),
               )


class Role(db.Model):
    r_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    r_name = db.Column(db.String(16))
    # 角色和用户一对一
    user_id = db.Column(db.Integer, db.ForeignKey('tb_user.u_id'), nullable=True)
    # 角色和权限多对多
    permission = db.relationship('Permission', secondary=r_p, backref='role')

    __tablename__ = 'tb_role'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
