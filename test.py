from models.user import User
from utils import log


def test():
    form = dict(
        username='test',
        password='123',
    )
    u = User.new(form)
    log(u.json())


if __name__ == '__main__':
    test()
