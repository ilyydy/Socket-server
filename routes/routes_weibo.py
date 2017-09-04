from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    http_response,
    current_user,
    login_required,
)
from utils import template, log


# 微博相关页面
def index(request):
    u = current_user(request)
    weibos = Weibo.find_all(user_id=u.id)
    body = template('weibo_index.html', weibos=weibos, user=u)
    return http_response(body)


def new(request):
    body = template('weibo_new.html')
    return http_response(body)


def add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    Weibo.new(form, u.id)
    return redirect('/weibo/index')


def delete(request):
    # 删除微博
    weibo_id = int(request.query.get('id', None))
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    # 生成一个 edit 页面
    body = template('weibo_edit.html', weibo=w)
    return http_response(body)


def update(request):
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    w = Weibo.find(weibo_id)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    Comment.new(form, u.id)
    return redirect('/weibo/index')


def same_user_required(route_function):

    def f(request):
        log('same user required', request)
        u = current_user(request)
        if request.method == 'GET':
            webbo_id = int(request.query.get('id'))
        else:
            webbo_id = int(request.form().get('id'))
        w = Weibo.find(webbo_id)
        if w.is_owner(u.id):
            return route_function(request)
        else:
            return redirect('/login')

    return f


def route_dict():
    r = {
        '/weibo/index': login_required(index),
        '/weibo/new': login_required(new),
        '/weibo/edit': login_required(same_user_required(edit)),
        '/weibo/add': login_required(add),
        '/weibo/update': login_required(same_user_required(update)),
        '/weibo/delete': login_required(same_user_required(delete)),
        '/comment/add': login_required(comment_add),
    }
    return r
