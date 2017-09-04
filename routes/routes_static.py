from routes import current_user, login_required
from routes import http_response
from utils import template, log


def route_index(request):
    """
    主页的处理函数, 返回主页的响应
    """
    u = current_user(request)
    log('current user', u)
    body = template('index.html', username=u.username)
    return http_response(body)


def route_static(request):
    """
    静态资源的处理函数, 读取静态文件并生成响应返回
    """
    filename = request.query.get('file', )
    path = 'static/' + filename
    with open(path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        binary = header + f.read()
        return binary


def route_dict():
    r = {
        '/': login_required(route_index),
        '/static': login_required(route_static),
    }
    return r
