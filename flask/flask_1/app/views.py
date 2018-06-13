from flask import render_template, Blueprint

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
