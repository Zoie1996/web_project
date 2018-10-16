from django.conf import settings
from urllib.parse import urlencode, parse_qs
from urllib.request import urlopen
import logging
import json

from .exceptions import QQAPIException
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer


logger = logging.getLogger('django')


class OAuthQQ(object):
    """
    用户登录的工具类
    提供了QQ登录可能用到的方法
    """
    def __init__(self, app_id=None, app_key=None, redirect_url=None, state=None):
        self.app_id = app_id or settings.QQ_APP_ID
        self.app_key = app_key or settings.QQ_APP_KEY
        self.redirect_url = redirect_url or settings.QQ_REDIRECT_URL
        self.state = state or settings.QQ_STATE

    def generate_qq_login_url(self):
        """
        拼接用户QQ登录的链接地址
        :return:
        """
        url = 'https://graph.qq.com/oauth2.0/authorize?'
        data = {
            'response_type': 'code',
            'client_id': self.app_id,
            'redirect_uri': self.redirect_url,
            'state': self.state,
            'scope': 'get_user_info'  # 获取用户QQ的openid
        }
        query_string = urlencode(data)
        url += query_string
        print(url)

        return url

    def get_access_token(self, code):
        """
        获取qq的access_token
        :param code: 调用接口的凭据
        :return: access_token
        """
        url = 'https://graph.qq.com/oauth2.0/token?'
        req_data = {
            'grant_type': 'authorization_code',
            'client_id': self.app_id,
            'client_secret': self.app_key,
            'code': code,
            'redirect_uri': self.redirect_url
        }
        url += urlencode(req_data)

        # 发送请求
        try:
            response = urlopen(url)
            # 读取QQ返回的响应体数据
            response = response.read().decode()
            # 将返回的查询字符串转换为字典
            response_dict = parse_qs(response)
            access_token = response_dict['access_token'][0]
        except Exception as e:
            logger.error(e)
            raise QQAPIException('获取access_token异常')

        return access_token

    def get_openid(self, access_token):
        """
        获取qq的openid
        :param access_token: 调用接口的凭据
        :return: openid
        """
        url = 'https://graph.qq.com/oauth2.0/me?access_token=' + access_token

        response_data = None
        try:
            response = urlopen(url)
            response_data = response.read().decode()
            # 返回的数据格式 callback( {"client_id":"YOUR_APPID","openid":"YOUR_OPENID"} )\n;
            # 截取需要的字符串
            data = json.loads(response_data[10: -4])
        except Exception:
            data = parse_qs(response_data)
            logger.error('code=%s msg=%s' % (data.get('code'), data.get('msg')))
            raise QQAPIException('获取openid异常')

        openid = data.get('openid', None)

        return openid
