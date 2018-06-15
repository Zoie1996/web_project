import os

import redis
from flask import Flask
from flask_session import Session

from app.models import db
from app.stu_views import stu_blueprint
from app.user_views import user


def create_app():
    # 定义静态文件路径
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')

    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    app.register_blueprint(blueprint=user, url_prefix='/')
    app.register_blueprint(blueprint=stu_blueprint, url_prefix='/stu')


    app.config['SECRET_KEY'] = "\xb1Lm\x81L\x0f\xd6H\xad"
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='119.27.166.245', port=9736, password='liutc1014?')
    app.config['SESSION_KEY_PREFIX'] = 'flask'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/flask_stu"
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = True

    Session(app=app)
    db.init_app(app=app)

    return app
