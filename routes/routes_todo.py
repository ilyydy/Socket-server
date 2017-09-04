from models.todo import Todo
from routes import (
    redirect,
    http_response,
    current_user,
    login_required,
)
from utils import template, log


def index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    body = template('todo_index.html')
    return http_response(body)


def route_dict():
    d = {
        '/todo/index': login_required(index),
    }
    return d
