import redis
from flask import Flask
from flask_session import Session

from App.house_views import house_blueprint
from App.user_views import user_blueprint
from App.models import db
from utils.setting import static_dir, templates_dir

se = Session()


def create_app():
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)
    # 配置数据库
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/aj"
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False
    db.init_app(app=app)

    # 配置session
    app.config['SECRET_KEY'] = "\xb1Lm\x81L\x0f\xd6H\xad"
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_REDIS'] = redis.Redis(host='119.27.166.245', port=9736, password='liutc1014?')
    app.config['SESSION_KEY_PREFIX'] = 'session'
    se.init_app(app=app)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=house_blueprint, url_prefix='/house')

    return app
