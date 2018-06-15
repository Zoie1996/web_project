from flask import Blueprint, render_template, session, redirect, url_for, request

from utils.decoration import is_login

user = Blueprint('user', __name__)

from app.models import db, User, Permission, Role


@user.route('/')
def index():
    return render_template('index.html')


@user.route('/create_db/')
def create_db():
    # 创建表
    db.create_all()
    return '创建表成功'


@user.route('/drop_db/')
def drop_db():
    # 删除表
    db.drop_all()
    return '删除表成功'


@user.route('/login/', methods=['GET', 'POST'])
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
                return redirect(url_for('user.index'))
            else:
                msg = '用户名或密码错误'
                return render_template('login.html', msg=msg)
        else:
            msg = '用户名错误'
            return render_template('login.html', msg=msg)


@user.route('/register/', methods=['GET', 'POST'])
def register():
    """
    注册
    """
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        password2 = request.form.get('password2')
        flag = True
        if not all([username, password, password2]):
            msg, flag = '请填写完整的注册信息', False
        if len(username) > 10:
            msg, flag = '用户名太长, 请重新输入', False
        if password != password2:
            msg, flag = '两次密码不一致', False
        if not flag:
            return render_template('register.html', msg=msg)
        user = User(username, password)
        user.save()
        return redirect(url_for('user.login'))


@user.route('/user/', methods=['GET'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return render_template('users.html', users=users)


@user.route('/del_user/<int:u_id>/', methods=['GET'])
def del_user(u_id):
    if request.method == 'GET':
        user = User.query.get(u_id)
        user.delete()
        return redirect(url_for('user.users'))


@user.route('/del_user_permission/<int:u_id>/<int:p_id>/', methods=['GET'])
def del_user_permission(u_id, p_id):
    if request.method == 'GET':
        user = User.query.get(u_id)
        permission = Permission.query.get(p_id)
        user.role.permission.remove(permission)
        db.session.commit()
        return redirect(url_for('user.users'))


@user.route('/roles/', methods=['GET'])
def roles():
    roles = Role.query.all()
    return render_template('roles.html', roles=roles)


@user.route('/del_role/<int:r_id>', methods=['GET'])
def del_role(r_id):
    """
    删除角色
    """
    role = Role.query.get(r_id)
    role.delete()
    return redirect(url_for('user.roles'))


@user.route('/add_role/', methods=['GET', 'POST'])
def add_role():
    """
    添加角色
    """
    if request.method == 'GET':
        permissions = Permission.query.all()
        return render_template('addroles.html', permissions=permissions)
    if request.method == 'POST':
        p_id_list = request.form.getlist('p_name')
        r_name = request.form.get('r_name')
        role = Role()
        role.r_name = r_name
        role.save()
        for p_id in p_id_list:
            p = Permission.query.get(int(p_id))
            role.permission.append(p)
        role.save()
        return redirect(url_for('user.roles'))


@user.route('/edit_role_premission/<int:r_id>/', methods=['GET', 'POST'])
def edit_role_premission(r_id):
    if request.method == 'GET':
        role = Role.query.get(r_id)
        permissions = Permission.query.all()

        return render_template('addroles.html', role=role, permissions=permissions)
    if request.method == 'POST':
        role = Role.query.get(r_id)
        db.session.commit()
        return redirect(url_for('user.roles'))
