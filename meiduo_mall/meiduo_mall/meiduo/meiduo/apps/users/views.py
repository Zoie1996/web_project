import re

from django_redis import get_redis_connection
from rest_framework import mixins
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.views import ObtainJSONWebToken

from carts.utils import merge_cart_cookie_to_redis
from goods.models import SKU
from goods.serializers import SKUSerializer
# Create your views here.
from users.models import User
from verifications.serializers import CheckImageCodeSerializer
from . import constants
from . import serializers
from .serializers import EmailSerializer
from .utils import get_user_by_account


class UsernameCountView(APIView):
    """
    统计用户名数量
    """
    def get(self, request: Request, username):
        """
        获取指定用户名数量
        :param request:
        :param username:
        :return:
        """
        count = User.objects.filter(username=username).count()

        data = {
            'username': username,
            'count': count
        }

        return Response(data)


class MobileCountView(APIView):
    """
    手机号数量
    """
    def get(self, request: Request, mobile):
        """
        统计指定手机号数量
        :param request:
        :param mobile:
        :return:
        """
        count = User.objects.filter(mobile=mobile).count()

        data = {
            'mobile': mobile,
            'count': count
        }

        return Response(data)


class UserView(CreateAPIView):
    """
    用户注册
    """
    queryset = User.objects.all()
    serializer_class = serializers.CreateUserSerializer


class SMSCodeTokenView(GenericAPIView):
    """
    获取发送短信验证码的凭据(找回密码第一步)
    """
    serializer_class = CheckImageCodeSerializer

    def get(self, request: Request, account):
        # 校验图片验证码
        serializer = self.get_serializer(data=request.query_params)  # type: Serializer
        serializer.is_valid(raise_exception=True)

        # 根据account查询User对象(account可能是用户名，所以使用get_object())
        user = get_user_by_account(account)  # type: User
        if not user:
            return Response({'message': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)

        # 根据User对象的手机号生成access_token
        access_token = user.generate_send_sms_code_token()

        # 修改手机号
        mobile = re.sub(r'(\d{3})\d{4}(\d{4})', r'\1****\2', user.mobile)

        return Response({
            'mobile': mobile,
            'access_token': access_token
        })


class PasswordTokenView(GenericAPIView):
    """
    生成用户账号设置密码的token
    """
    serializer_class = serializers.CheckSMSCodeSerializer

    def get(self, request: Request, account):
        """
        根据用户账号获取修改密码的token
        :param request:
        :param account:
        :return:
        """
        # 校验短信验证码
        serializer = self.get_serializer(data=request.query_params)  # type: Serializer
        serializer.is_valid(raise_exception=True)

        user = serializer.user

        # 生成修改用户密码的access_token
        access_token = user.generate_set_password_token()

        return Response({'user_id': user.id, 'access_token': access_token})


class PasswordView(mixins.UpdateModelMixin, GenericAPIView):
    """
    用户密码重置(重置POST 修改PUT)
    """
    queryset = User.objects.all()
    serializer_class = serializers.ResetPasswordSerializer

    def post(self, request, pk):
        return self.update(request, pk)


class UserDetailView(RetrieveAPIView):
    """
    用户详情
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserDetailSerializer
    permission_classes = [IsAuthenticated]  # 已通过认证(登录成功)的用户才能访问该视图

    def get_object(self):
        """
        该方法只能获得url路径参数中的pk，而我们定义的路由中并没有路径参数，需要重写该方法
        request以属性的形式被保存在类视图对象中，可以被类视图的各种请求所调用
        所有继承自APIView的类视图，在进入视图之前，都会经过drf的各种认证，
        并将认证解析出来的用户以user属性保存在request对象中
        类视图对象还有kwargs属性，是将url的路径参数以键值对的形式保存在该属性之中
        :return: user
        """
        return self.request.user


class EmailView(UpdateAPIView):
    """
    保存邮箱
    """
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    # 也可以通过重写get_serializer方法实现，因为序列化器对象中的实例是通过get_object获得
    # def get_serializer(self, *args, **kwargs):
    #     return EmailSerializer(self.request.user, data=self.request.data)


class EmailVerifyView(APIView):
    """
    邮箱验证
    """
    def get(self, request: Request):
        # 获取邮箱链接中的token
        token = request.query_params.get('token')
        if not token:
            return Response({'message': '缺少token'}, status=status.HTTP_400_BAD_REQUEST)

        # 使用序列化器校验
        result = User.check_email_verify_token(token)
        # 保存
        if not result:
            return Response({'message': '非法的token'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'OK'})


class AddressViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    """
    用户地址新增与修改
    """
    serializer_class = serializers.UserAddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.addresses.filter(is_deleted=False)

    def list(self, request: Request, *args, **kwargs):
        """
        用户地址列表数据
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        queryset = self.get_queryset()
        serializer = serializers.UserAddressSerializer(queryset, many=True)
        user = request.user

        return Response({
            'user_id': user.id,
            'default_address_id': user.default_address_id,
            'limit': constants.USER_ADDRESS_COUNTS_LIMIT,
            'addresses': serializer.data
        })

    def create(self, request, *args, **kwargs):
        """
        保存用户地址数据(之所以重写该序列化器的create方法，是因为要将地址对应用户信息发送出去)
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 检查用户地址数据数目不能超过上限
        count = request.user.addresses.count()
        if count >= constants.USER_ADDRESS_COUNTS_LIMIT:
            return Response({'message': '保存地址数据已达到上限'}, status=status.HTTP_400_BAD_REQUEST)
        # 序列化器已经完成了地址的创建以及用户的绑定，这里仅需调用父类的create方法来执行序列化器的反序列化工作
        return super().create(request, *args, **kwargs)

    def destroy(self, request: Request, *args, **kwargs):
        """
        删除地址
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        address = self.get_object()

        # 进行逻辑删除
        address.is_deleted = True
        address.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['put'], detail=True)
    def status(self, request: Request, pk=None, address_id=None):
        """
        设置默认地址
        :param request:
        :param pk:
        :param address_id:
        :return:
        """
        address = self.get_object()
        request.user.default_address = address
        request.user.save()

        return Response({'message': 'OK'}, status=status.HTTP_200_OK)

    @action(methods=['put'], detail=True)
    def title(self, request: Request, pk=None, address_id=None):
        """
        修改标题
        :param request:
        :param pk:
        :param address_id:
        :return:
        """
        address = self.get_object()
        serializer = serializers.AddressTitleSerializer(instance=address, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class BrowseHistory(mixins.CreateModelMixin, GenericAPIView):
    """用户浏览历史记录"""
    serializer_class = serializers.AddHistorySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        """
        保存
        :param request:
        :return:
        """
        return self.create(request)

    def get(self, request: Request):
        user_id = request.user.id

        # 查询redis数据库
        redis_conn = get_redis_connection('history')
        sku_ids = redis_conn.lrange('history_%s' % user_id, 0, constants.USER_BROWSE_HISTORY_LIMIT - 1)

        # 根据redis返回的sku_id查询数据
        sku_list = []
        for sku_id in sku_ids:
            sku = SKU.objects.get(id=sku_id)
            sku_list.append(sku)

        # 使用序列化器序列
        serializer = SKUSerializer(sku_list, many=True)
        return Response(serializer.data)
    
    
class UserAuthorization(ObtainJSONWebToken):
    """
    将购物车合并逻辑添加到登录逻辑中
    """
    def post(self, request, *args, **kwargs):
        # 调用jwt对用户登录的数据进行验证
        # 如果用户登录成功，进行购物车数据合并
        
        response = super(ObtainJSONWebToken, self).post(request)
        
        # 取出用户对象
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # 表示用户登录成功
            user = serializer.validated_data.get('user')
            # 合并购物车
            response = merge_cart_cookie_to_redis(request, response, user)
            
        return response