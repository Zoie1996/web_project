from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework_jwt.settings import api_settings

from carts.utils import merge_cart_cookie_to_redis
from .exceptions import QQAPIException
from .models import OauthQQUser
from .serializers import OAuthQQUserSerializer
from .utils import OAuthQQ


# Create your views here.


class OAuthQQUrlView(APIView):
    """
    提供QQ登录的网址: /oauth/qq/authorization/?state=xxxx
    state为QQ登录成功后，后端引导用户到哪个页面
    """
    def get(self, request: Request):
        # 提取state参数
        state = request.query_params.get('state')
        if not state:
            state = '/'  # 如果前端未指明，指定用户登录QQ成功后跳转到主页

        # 提取QQ说明文档，拼接用户QQ登录的链接地址
        oauth_qq = OAuthQQ(state=state)
        login_url = oauth_qq.generate_qq_login_url()

        # 返回链接地址
        return Response({'oauth_url': login_url})


class OAuthQQUserView(GenericAPIView):
    """
    获取QQ用户对应的美多商城用户
    """
    serializer_class = OAuthQQUserSerializer

    def get(self, request: Request):
        # 提取code参数
        code = request.query_params.get('code')
        if not code:
            return Response({'message': '缺少code'}, status=status.HTTP_400_BAD_REQUEST)

        # 凭借code向QQ服务器发起请求，获取access_token
        oauth_qq = OAuthQQ()
        try:
            access_token = oauth_qq.get_access_token(code)

            # 凭借access_token向QQ服务器发起请求，获取openid
            openid = oauth_qq.get_openid(access_token)
        except QQAPIException:
            return Response({'message': '获取QQ用户数据异常'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        # 凭借openid查询此用户是否绑定过美多用户
        try:
            oauth_user = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            access_token = OauthQQUser.generate_save_user_token(openid)
            return Response({'access_token': access_token})
        else:
            user = oauth_user.user
            # 如果已经绑定，为用户生成JWT token凭证
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            response = Response({
                'token': token,
                'username': user.username,
                'user_id': user.id
            })
            response = merge_cart_cookie_to_redis(request, response, user)
            
            return response

    def post(self, request: Request):
        """
        调用序列化器检查数据
        :param request:
        :return:
        """
        serializer: Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # 保存用户对象与openid的对应关系
        user = serializer.save()

        # 返回用户登录成功的JWT token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        response = Response({
            'token': token,
            'username': user.username,
            'user_id': user.id
        })
        response = merge_cart_cookie_to_redis(request, response, user)

        return response
