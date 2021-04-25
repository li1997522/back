# 定义使用flask_restful框架的api路由

from flask import Blueprint
from flask_restful import Api
from app_demo.app_api_v1.todo_api import Todo, TodoList

api_bp = Blueprint('flask_restful_api', __name__)
api = Api(api_bp)

# Route
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
