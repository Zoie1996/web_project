from functools import wraps

from flask import redirect, url_for, session


def is_login(func):
    """
    装饰器用于登录验证
    """

    @wraps(func)
    def check_login():
        if session.get('user_id'):
            return func()
        else:
            # 验证失败
            return redirect(url_for('user.login'))
    return check_login
