# 统一错误处理
from flask import Blueprint, jsonify

errors = Blueprint('common', __name__)


@errors.app_errorhandler(404)
def not_found(e):
    print(e)
    error_info = '{}'.format(e)
    response = jsonify({'error': error_info})
    response.status_code = 404
    return response


@errors.app_errorhandler(403)
def forbidden(e):
    print(e)
    error_info = '{}'.format(e)
    response = jsonify({'error': error_info})
    response.status_code = 403
    return response

# 未查找到数据
@errors.app_errorhandler(410)
def gone(e):
    print(e)
    error_info = '{}'.format(e)
    response = jsonify({'error': error_info})
    response.status_code = 410
    return response
