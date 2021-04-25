# 用于配置项目相关信息


class Config:
    SECRET_KEY = 'secret key'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    @staticmethod
    def init_app(app):
        pass


class MySQLConfig:
    MYSQL_USERNAME = 'root'
    MYSQL_PASSWORD = '123456'
    MYSQL_HOST = 'localhost'
    DATABASE = 'rest_db'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, MySQLConfig.DATABASE)


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, MySQLConfig.DATABASE)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}/{}'.format(MySQLConfig.MYSQL_USERNAME,
                                                                   MySQLConfig.MYSQL_PASSWORD,
                                                                   MySQLConfig.MYSQL_HOST, MySQLConfig.DATABASE)


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
    'JSON_AS_ASCII': False
}
# 解决中文编码的问题
config.update(RESTFUL_JSON=dict(ensure_ascii=False))

swagger_config = {
    "headers": [
        ],
        "specs": [
            {
                "endpoint": 'apispec_2',
                "route": '/apispecification.json',
                "rule_filter": lambda rule: True,  # all in
                "model_filter": lambda tag: True,  # all in
            }
        ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/doc/"
}
template_config = {
  "info": {
    "title": "Sample API",
    "description": "Hahaha, this is a API kingdom!",
    "version": "1.0.0"
  }
}
