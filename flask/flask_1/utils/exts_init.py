# from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from flask_session import Session

from app.models import db

# toolbar = DebugToolbarExtension()
api = Api()
se = Session()


def ext_init(app):
    # 配置session
    # 第一种方式
    # se = Session()
    se.init_app(app=app)

    # 配置session
    # Session(app=app)

    # 初始化数据库
    db.init_app(app=app)
    app.debug = True
    # toolbar.init_app(app=app)
    api.init_app(app=app)
