from functools import wraps

from flask import redirect, url_for, session


def is_login(func):
    @wraps(func)
    def check_login():
        user_session = session.get('user_id')
        if user_session:
            return func()
        else:
            return redirect(url_for('user.login'))
    return check_login
