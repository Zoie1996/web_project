import os
import re

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for

from App.models import User, db
from utils import status_code
from utils.setting import UPLOAD_DIR
from utils.decoration import is_login

user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/register/', methods=['GET'])
def register():
    return render_template('register.html')


@user_blueprint.route('/register/', methods=['POST'])
def user_register():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    password2 = request.form.get('password2')
    # 1. 验证数据完整性
    if not all([mobile, password, password2]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
    # 2. 验证手机号码正确性
    if not re.match(r'^1[345678]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    # 3. 验证密码
    if password != password2:
        return jsonify(status_code.USER_REGISTER_PASSWORD_IS_NOT_VALID)

    # 4. 保存用户数据
    user = User.query.filter(User.phone == mobile).first()
    if user:
        return jsonify(status_code.USER_REGISTER_IS_LOGIN)
    else:
        user = User()
        user.phone = mobile
        user.password = password
        user.name = mobile
        user.add_update()
        return jsonify(status_code.SUCCESS)


@user_blueprint.route('/login/', methods=['GET'])
def login():
    return render_template('login.html')


@user_blueprint.route('/login/', methods=['POST'])
def user_login():
    mobile = request.form.get('mobile')
    password = request.form.get('password')
    # 1. 验证数据完整
    if not all([mobile, password]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)
    # 2. 验证手机正确性
    if not re.match(r'^1[345678]\d{9}$', mobile):
        return jsonify(status_code.USER_REGISTER_MOBILE_ERROR)
    user = User.query.filter(User.phone == mobile).first()
    # 3. 验证用户
    if user:
        if not user.check_pwd(password):
            return jsonify(status_code.USER_LOGIN_PASSWORD_IS_NOT_VALID)
        # 4. 验证用户成功
        session['user_id'] = user.id
        return jsonify(status_code.SUCCESS)
    else:
        return jsonify(status_code.USER_LOGIN_USER_NOT_EXISTS)


@user_blueprint.route('/logout/', methods=['GET'])
@is_login
def user_logout():
    session.clear()
    return redirect(url_for('user.login'))


@user_blueprint.route('/profile/', methods=['GET'])
@is_login
def profile():
    return render_template('profile.html')


@user_blueprint.route('/profile/', methods=['PATCH'])
@is_login
def user_profile():
    # 更改头像
    file = request.files.get('avatar')
    if not re.match(r'image/.*', file.mimetype):
        return jsonify(status_code.USER_CHANGE_PROFILE_IMAGE)
    image_path = os.path.join(UPLOAD_DIR, file.filename)
    file.save(image_path)
    user = User.query.get(session['user_id'])
    avatar_path = os.path.join('upload', file.filename)
    user.avatar = avatar_path
    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify({'code': status_code.OK, 'image_url': avatar_path})


@user_blueprint.route('/change_name/', methods=['POST'])
@is_login
def change_name():
    # 更改昵称
    name = request.form.get('name')
    # 过滤用户是否存在
    if User.query.filter(User.name == name).first():
        return jsonify(status_code.USER_CHANGE_NAME_IS_VALID)
    # 获取当前用户
    user = User.query.get(session['user_id'])
    user.name = name
    try:
        user.add_update()
    except Exception as e:
        db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)
    return jsonify(status_code.SUCCESS)


@user_blueprint.route('/my/', methods=['GET'])
@is_login
def my():
    return render_template('my.html')


@user_blueprint.route('/show_my/', methods=['GET'])
@is_login
def show_my():
    """
    展示用户信息
    """
    user = User.query.get(session['user_id'])
    return jsonify({'code': status_code.OK, 'data': user.to_basic_dict()})


@user_blueprint.route('/auth/', methods=['GET'])
def auth():
    return render_template('auth.html')


@user_blueprint.route('/auth/', methods=['POST'])
@is_login
def user_auth():
    real_name = request.form.get('real_name')
    id_card = request.form.get('id_card')
    if not all([real_name, id_card]):
        return jsonify(status_code.USER_REGISTER_DATA_NOT_NULL)

    if not re.match(r'(^\d{15}$)|(^\d{18}$)|(^\d{17}(\d|X|x)$)', id_card):
        return jsonify(status_code.USER_AUTH_ID_CARD_IS_VALID)

    user = User.query.get(session['user_id'])
    user.id_name = real_name
    user.id_card = id_card
    user.add_update()
    return jsonify(status_code.SUCCESS)
