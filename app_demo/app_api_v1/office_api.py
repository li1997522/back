from flask import Blueprint, Flask, abort
from app_demo.models.office import Office

# 定义蓝图，然后在config/__init__.py中注册
office_app = Blueprint('office_bp', __name__, url_prefix='/api/office')


@office_app.route('/', methods={'get'})
def offices():
    # abort(403)
    return 'Hello World! my office我的'
