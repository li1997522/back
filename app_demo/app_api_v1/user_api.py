from datetime import datetime

from flask import Blueprint, jsonify, abort, request
from sqlalchemy import text, bindparam, Integer

from app_demo.models.user import User
from app_demo.config import db

# 定义蓝图，然后在config/__init__.py中注册
from app_demo.dto.userDto import UserDto
from flasgger import swag_from

user_app = Blueprint('user_bp', __name__, url_prefix='/api')
session = db.session

@swag_from("user_api_get.yml")
@user_app.route('/user/<int:user_id>', methods={'get'})
def get(user_id):
    print(user_id)
    # user = User.query.filter_by(id=user_id).first()
    # 第一种参数方式
    # sql = 'select * from user where id={}'
    # result = session.execute(sql.format(user_id))
    # 第二各参数方式
    sql = 'select id,name,age,address,create_time as createTime from user where id= :id'
    # result = session.execute(text(sql), {'id': user_id})
    # 第三种指定参数类型，不然默认都是字符串
    #    date_param=datetime.today()+timedelta(days=-1*10)
    #    t=text(sql, bindparams=[bindparam('create_time', type_=DateTime, required=True)])
    t = text(sql, bindparams=[bindparam('id', type_=Integer, required=True)])
    result = session.execute(t, {'id': user_id})
    ret = result.first()
    result.close()
    print(ret)
    if ret is not None:
        # print(UserDto(**ret).__repr__())
        return jsonify(UserDto(**ret).__repr__())
    else:
        abort(410, '未查询到数据')
        return


@user_app.route('/user/<int:pageSize>/<int:pageNum>', methods={'get'})
def list(pageSize, pageNum):
    # user_list = User.query.all()
    # return jsonify(list(map(User.user2dict, user_list)))
    if pageSize < 1:
        pageSize = 1
    if pageNum < 1:
        pageNum = 1
    record = pageSize * (pageNum - 1)
    sql = 'select id,name,age,address,create_time as createTime from user limit {},{}'.format(record, pageSize)
    sqlCount = 'select count(id) from user'
    print(sql)
    result = session.execute(text(sql))
    output = []
    ret = result.fetchall()
    total = session.execute(text(sqlCount)).first()[0]
    print(total)
    for row in ret:
        output.append(UserDto(**row).__repr__())
    result.close()
    mod = total % pageSize
    if mod == 0:
        pages = total // pageSize
    else:
        pages = total // pageSize + 1
    pageData = {'total': total, 'pageSize': pageSize, 'pageNum': pageNum, 'pages': pages, 'list': output}
    return jsonify(pageData)


@user_app.route('/user/<int:user_id>', methods={'put'})
def update(user_id):
    # user = User.query.filter_by(id=user_id).first()
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(410)
    try:
        user_info = request.get_json()
        user.name = user_info['name']
        user.address = user_info['address']
        session.commit()
    except:
        session.rollback()
    return jsonify(User.user2dict(user)), 200


@user_app.route('/user', methods={'post'})
def add():
    try:
        user_info = request.get_json()
        print(user_info)
        print(datetime.now())
        user = User(name=user_info['name'], age=user_info['age'], address=user_info['address'],
                    create_time=datetime.now())
        session.add(user)
        session.commit()
    except ValueError:
        print(ValueError)
        session.rollback()
        return {'code': 'error'}
    return {'code': 'success'}, 201


@user_app.route('/user/<int:user_id>', methods={'delete'})
def delete(user_id):
    user = User.query.filter_by(id=user_id)
    if not any(user):
        abort(404)
    try:
        user.delete()
        session.commit()
    except:
        session.rollback()
    return {'code': 'success'}, 204
