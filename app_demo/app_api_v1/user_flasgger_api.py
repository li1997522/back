import re
from flask import Blueprint, jsonify, abort, request
from sqlalchemy import text
from sqlalchemy.util import NoneType

from app_demo.models.user import User
from app_demo.config import db

from app_demo.dto.userDto import UserDto
from flasgger import swag_from

user_app2 = Blueprint('user_bp', __name__, url_prefix='/')
session = db.session


@swag_from("user_api_get.yml")
@user_app2.route('/users/<int:id>', methods={'get'})
def get(id):
    print(id)
    sql = 'select * from user where id={}'
    result = session.execute(sql.format(id))
    ret = result.first()
    result.close()
    print(ret)
    if ret is not None:
        return jsonify(UserDto(**ret).__repr__())
    else:
        return {'code': 'not_exist', 'msg': '用户信息不存在'}, 410

@swag_from("user_api_list.yml")
@user_app2.route('/users', methods={'get'})
def list():
    searchKey = request.args.get('searchKey')
    print(searchKey)
    sql = ''
    if searchKey is NoneType or searchKey is None:
        sql = 'select id,name,address from user'
    else:
        sql = 'select id,name,address from user where name like "%{}%"'.format(searchKey)
    print(sql)
    result = session.execute(text(sql))
    output = []
    ret = result.fetchall()
    for row in ret:
        output.append(UserDto(**row).__repr__())
    result.close()

    return jsonify(output), 200


@swag_from("user_api_update.yml")
@user_app2.route('/users/<int:id>', methods={'put'})
def update(id):
    user = User.query.filter_by(id=id).first()
    if user is None:
        return {'code': 'not_exist', 'msg': '用户信息不存在'}, 410
    try:
        user_info = request.get_json()
        user.name = user_info['name']
        user.address = user_info['address']
        if len(user.name) < 3 or len(user.name) > 32:
            return {'code': 'fail', 'msg': '用户名长度为3到32个字符'}, 400
        pattern = "^[a-z0-9A-Z]+$"
        print(re.match(pattern, user.name))
        if re.match(pattern, user.name) is None:
            return {'code': 'fail', 'msg': '用户名只能包含数字和大小写字母'}, 400
        if len(user.address) < 6 or len(user.address) > 1000:
            return {'code': 'fail', 'msg': '地址长度为6到1000个字符'}, 400
        session.commit()
    except:
        session.rollback()
    return {'code': 'success', 'msg': '用户更新成功'}, 201


@swag_from("user_api_add.yml")
@user_app2.route('/users', methods={'post'})
def add():
    try:
        user_info = request.get_json()
        name = user_info['name']
        if len(name) < 3 or len(name) > 32:
            return {'code': 'fail', 'msg': '用户名长度为3到32个字符'}, 400
        print(name)
        pattern = "^[a-z0-9A-Z]+$"
        print(re.match(pattern, name))
        if re.match(pattern, name) is None:
            return {'code': 'fail', 'msg': '用户名只能包含数字和大小写字母'}, 400
        address = user_info['address']
        if len(address) < 6 or len(address) > 1000:
            return {'code': 'fail', 'msg': '地址长度为6到1000个字符'}, 400
        user = User(name=name, address=address)
        session.add(user)
        session.commit()
    except ValueError:
        print(ValueError)
        session.rollback()
        return {'code': 'error'}, 500
    return {'code': 'success', 'msg': '用户添加成功'}, 201


@user_app2.route('/users/<int:id>', methods={'delete'})
@swag_from("user_api_delete.yml")
def delete(id):
    user = User.query.filter_by(id=id)
    if not any(user):
        return {'code': 'not_exist', 'msg': '用户信息不存在'}, 410
        return
    try:
        user.delete()
        session.commit()
    except:
        session.rollback()
        return {'code': 'fail', 'msg': '用户删除失败'}, 500
    return {'code': 'success', 'msg': '用户删除成功'}, 200
