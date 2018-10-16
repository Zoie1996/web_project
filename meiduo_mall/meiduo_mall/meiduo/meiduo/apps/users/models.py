from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer as TJWSSerializer, BadData

from meiduo.utils.models import BaseModel
from . import constants


# Create your models here.
class User(AbstractUser):
    """
    用户信息
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')
    email_active = models.BooleanField(default=False, verbose_name='邮箱验证状态')
    default_address = models.ForeignKey('Address', related_name='users', null=True, blank=True,
                                        on_delete=models.SET_NULL, verbose_name='默认地址')

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def generate_send_sms_code_token(self):  # access_token与用户对象相关，所以将此方法定义在用户对象模型下
        """
        生成发送短信验证码的access_token
        :return: access_token
        """
        # 创建itsdangerous模型转换工具
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.SEND_SMS_CODE_TOKEN_EXPIRES)
        data = {
            'mobile': self.mobile
        }
        # 将字典数据传入生成token
        token = serializer.dumps(data)  # type: bytes
        return token.decode()

    @staticmethod
    def check_send_sms_code_token(token):
        """
        检验access_token
        :param token:
        :return: Mobile None
        """
        # 创建itsdangerous模型的转换工具
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.SEND_SMS_CODE_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return None
        else:
            mobile = data.get('mobile')
            return mobile

    def generate_set_password_token(self):
        """
        生成修改密码的token
        :return:
        """
        # 创建itsdangerous模型转换工具
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.SET_PASSWORD_TOKEN_EXPIRES)
        data = {
            'user_id': self.id
        }
        # 将字典数据传入生成token
        token = serializer.dumps(data)  # type: bytes
        return token.decode()

    @staticmethod
    def check_set_password_token(token, user_id):
        """
        检验设置密码的token
        :param token:
        :param user_id:
        :return:
        """
        serializer = TJWSSerializer(settings.SECRET_KEY, constants.SET_PASSWORD_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return False
        else:
            if user_id != str(data.get('user_id')):
                return False
            else:
                return True

    def generate_email_verify_url(self):
        """生成邮箱验证链接"""
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.EMAIL_VERIFY_TOKEN_EXPIRES)
        data = {
            'user_id': self.id,
            'email': self.email
        }
        token = serializer.dumps(data).decode()

        verify_url = 'http://www.meiduo.site:8080/success_verify_email.html?token=' + token

        return verify_url

    @staticmethod
    def check_email_verify_token(token):
        serializer = TJWSSerializer(settings.SECRET_KEY, expires_in=constants.EMAIL_VERIFY_TOKEN_EXPIRES)
        try:
            data = serializer.loads(token)
        except BadData:
            return False
        email = data.get('email')
        user_id = data.get('user_id')

        User.objects.filter(id=user_id, email=email).update(email_active=True)

        return True


class Address(BaseModel):
    """
    用户地址
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses', verbose_name='用户')
    title = models.CharField(max_length=20, verbose_name='地址名称')
    receiver = models.CharField(max_length=20, verbose_name='收货人')
    # 如果是跨应用的外键，在不导包的情况下可以使用字符串关联(应用名.模型类名)
    # related_name是进行反向关联时查询的属性，可以通过 Area 对象的 province_addresses 属性获取所有相关的 province 数据
    province = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='province_addresses',
                                 verbose_name='省')
    city = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='city_addresses', verbose_name='市')
    district = models.ForeignKey('areas.Area', on_delete=models.PROTECT, related_name='district_addresses',
                                 verbose_name='区')
    place = models.CharField(max_length=50, verbose_name='地址')
    mobile = models.CharField(max_length=11, verbose_name='手机')
    tel = models.CharField(max_length=20, null=True, blank=True, default='', verbose_name='固定电话')
    email = models.CharField(max_length=30, null=True, blank=True, default='', verbose_name='电子邮箱')
    is_deleted = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'tb_address'
        verbose_name = '用户地址'
        verbose_name_plural = verbose_name
        # 默认排序方式
        ordering = ['-update_time']
