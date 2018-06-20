from flask import render_template, Blueprint, make_response

# 导入蓝本 main_blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@main_blueprint.route('/')
def index():
    return render_template('index.html')


@main_blueprint.route('/hellostr/<name>/')
def show_str(name):
    return render_template('hello.html', name=name)


@main_blueprint.route('/helloint/<int:id>/')
def show_int(id):
    return render_template('hello.html', id=id)


@main_blueprint.route('/hellouuid/<uuid:uuid>/')
# 36e4eb8c-6d22-11e8-ae3a-acbc32d27f87 唯一ID
def show_uuid(uuid):
    return render_template('hello.html', uuid=uuid)


@main_blueprint.route('/hellofloat/<float:float>/')
def show_float(float):
    return render_template('hello.html', float=float)


@main_blueprint.route('/hellopath/<path:path>/')
def show_path(path):
    return render_template('hello.html', path=path)


@main_blueprint.route('/scores/', methods=['GET'])
def stu_scores():
    scores = [1, 2, 3, 4, 5]
    content_h2 = '<h2>哈哈哈</h2>'
    content_h3 = ' <h3>哈哈哈</h3> '
    return render_template('score.html', scores=scores, content_h2=content_h2, content_h3=content_h3)


@main_blueprint.route('/setcookie/')
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


@main_blueprint.route('/delcookie/')
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
