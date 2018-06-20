import os

import redis
from flask import Flask

from app.user_views import user_blueprint
from app.views import main_blueprint
from utils.exts_init import ext_init




def create_app():
    # 定义静态文件路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    #  注册app
    app.register_blueprint(blueprint=main_blueprint, url_prefix='/main')
    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')

    # SECRET_KEY 秘钥
    app.config['SECRET_KEY'] = "\xb1Lm\x81L\x0f\xd6H\xad"
    # session类型为redis
    app.config['SESSION_TYPE'] = 'redis'
    # 链接redis
    app.config['SESSION_REDIS'] = redis.Redis(host='119.27.166.245', port=9736, password='liutc1014?')
    # 添加session前缀
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    # 初始化数据库文件
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flask"
    # 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = True



    ext_init(app)
    return app
