import os

from flask import Flask
from App.user_views import user_blueprint
from App.models import db

def create_app():


    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    static_dir = os.path.join(BASE_DIR, 'static')
    templates_dir = os.path.join(BASE_DIR, 'templates')
    app = Flask(__name__,
                static_folder=static_dir,
                template_folder=templates_dir)

    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/aj"
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False
    db.init_app(app=app)


    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    return app
