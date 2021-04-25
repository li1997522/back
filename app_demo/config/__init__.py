from flasgger import Swagger
from flask import Flask
from app_demo.config.config import config, template_config, swagger_config
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app=app)
    db.init_app(app=app)
    Swagger(app, template=template_config, config=swagger_config)

    # 统一错误处理
    from .errors import errors
    app.register_blueprint(errors)

    # 注册到蓝图
    from app_demo.app_api_v1.office_api import office_app
    app.register_blueprint(office_app)

    from app_demo.app_api_v1.user_api import user_app
    app.register_blueprint(user_app)

    from app_demo.app_api_v1.user_flasgger_api import user_app2
    app.register_blueprint(user_app2)
    # 注册使用flask_restful框架的路由
    from app_demo.routes.routes import api_bp
    app.register_blueprint(api_bp)

    return app
