import re

from django.contrib.auth.backends import ModelBackend

from .models import User


def jwt_response_payload_handler(token, user=None, request=None):
    """
    重写obtain_jwt_token的返回值(默认只返回token)
    :param token:
    :param user:
    :param request:
    :return:
    """
    return {
        'user_id': user.id,
        'username': user.username,
        'token': token
    }


def get_user_by_account(account):
    """
    根据账号信息查找用户对象
    :param account: 手机号、用户名
    :return: User对象，None
    """
    try:
        if re.match(r'^1[3-9]\d{9}$', account):
            user = User.objects.get(mobile=account)
        else:
            user = User.objects.get(username=account)
    except User.DoesNotExist:
        return None
    else:
        return user


class UsernameMobileAuthBackend(ModelBackend):
    """
    重写认证系统的认证方法(默认只支持用户名，重写之后既支持用户名，也支持手机号登录)
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        # 根据username查询用户对象
        user = get_user_by_account(username)
        # 如果用户对象存在，调用check_password()方法检查密码
        if user and user.check_password(password):
            # 验证成功，返回对象
            return user
