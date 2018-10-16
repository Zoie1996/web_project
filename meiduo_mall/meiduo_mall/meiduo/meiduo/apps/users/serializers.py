import re

from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from celery_tasks.emails.tasks import send_verify_email
from goods.models import SKU
from users import constants
from users.models import User, Address
from users.utils import get_user_by_account


class CreateUserSerializer(serializers.ModelSerializer):
    """
    创建用户序列化器
    """
    password2 = serializers.CharField(label='确认密码', required=True, allow_null=False, allow_blank=False, write_only=True)
    sms_code = serializers.CharField(label='短信验证码', required=True, allow_null=False, allow_blank=False, write_only=True)
    allow = serializers.CharField(label='同意协议', required=True, allow_null=False, allow_blank=False, write_only=True)
    token = serializers.CharField(label='登录状态token', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'password2', 'sms_code', 'mobile', 'allow', 'token')
        extra_kwargs = {
            'id': {'read_only': True},
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的用户名',
                    'max_length': '仅允许5-20个字符的用户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate_mobile(self, value):
        """
        验证手机号
        :param value:
        :return:
        """
        if not re.match(r'^1[345789]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')
        return value

    def validate_allow(self, value):
        """
        验证用户是否同意协议
        :param value:
        :return:
        """
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议')
        return value

    def validate(self, attrs):
        """
        两次密码的验证
        :param attrs:
        :return:
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入密码不一致')

        # 判断短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']

        sms_code_server = redis_conn.get('sms_%s' % mobile)  # type: bytes
        if sms_code_server is None:
            raise serializers.ValidationError('无效的短信验证码')
        if sms_code_server.decode() != attrs['sms_code']:
            raise serializers.ValidationError('短信验证码错误')

        return attrs

    def create(self, validated_data):
        """
        创建用户
        :param validated_data:
        :return:
        """
        # 移除数据库模型中不存在的属性
        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        user = super(CreateUserSerializer, self).create(validated_data)

        # 调用认证系统加密密码
        user.set_password(validated_data['password'])
        user.save()

        # 手动为用户生成jwt
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 将token保存到user对象中，随着返回值返回给前端
        user.token = token

        return user


class CheckSMSCodeSerializer(serializers.Serializer):
    """
    检查sms_code
    """
    smscode = serializers.CharField(min_length=6, max_length=6)

    def validate_smscode(self, value):
        account = self.context['view'].kwargs['account']

        # 获取user
        user = get_user_by_account(account)  # type: User
        if not user:
            raise serializers.ValidationError('用户不存在')

        # 将user对象保存在序列化器对象中
        self.user = user

        redis_conn = get_redis_connection('verify_codes')
        sms_code_server = redis_conn.get('sms_%s' % user.mobile)  # type: bytes

        if not sms_code_server:
            raise serializers.ValidationError('无效的短信验证码')

        if sms_code_server.decode() != value:
            raise serializers.ValidationError('短信验证码错误')

        return value


class ResetPasswordSerializer(serializers.ModelSerializer):
    """
    校验密码
    """
    password2 = serializers.CharField(label='确认密码', write_only=True)
    access_token = serializers.CharField(label='操作token', write_only=True)

    class Meta:
        model = User
        fields = ('id', 'password', 'password2', 'access_token')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    def validate(self, attrs):
        """
        校验密码
        :param attrs:
        :return:
        """
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致')

        # 对比access_token中的用户id与请求的用户id是否一致
        allow = User.check_set_password_token(attrs['access_token'], self.context['view'].kwargs['pk'])
        if not allow:
            raise serializers.ValidationError('无效的access_token')

        return attrs

    def update(self, instance: User, validated_data):
        """
        更新密码
        :param instance:
        :param validated_data:
        :return:
        """
        instance.set_password(validated_data['password'])
        instance.save()

        return instance


class UserDetailSerializer(serializers.ModelSerializer):
    """
    用户详情序列化器
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'email_active')


class EmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')
        extra_kwargs = {
            'email': {
                'required': True
            }
        }

    def update(self, instance: User, validated_data):
        # 序列化器只帮助保存邮箱，并不会为我们发送邮件，需要重写
        email = validated_data['email']
        instance.email = email
        instance.save()

        # 生成激活链接
        verify_url = instance.generate_email_verify_url()

        # 发送验证邮件
        send_verify_email.delay(email, verify_url)

        return instance


class UserAddressSerializer(serializers.ModelSerializer):
    """
    用户地址序列化器
    """
    province = serializers.StringRelatedField(read_only=True)
    city = serializers.StringRelatedField(read_only=True)
    district = serializers.StringRelatedField(read_only=True)
    province_id = serializers.IntegerField(label='省ID', required=True)
    city_id = serializers.IntegerField(label='市ID', required=True)
    district_id = serializers.IntegerField(label='区ID', required=True)
    mobile = serializers.RegexField(label='手机号', regex=r'^1[3-9]\d{9}$')

    class Meta:
        model = Address
        exclude = ('user', 'is_deleted', 'create_time', 'update_time')

    def create(self, validated_data):
        """保存收货地址"""
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)


class AddressTitleSerializer(serializers.ModelSerializer):
    """
    地址标题
    """
    class Meta:
        model = Address
        fields = ('title',)


class AddHistorySerializer(serializers.Serializer):
    sku_id = serializers.IntegerField(min_value=1)

    def validate_sku_id(self, value):
        try:
            SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('sku_id不存在')
        return value

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        sku_id = validated_data['sku_id']

        # 清楚sku_id在redis中的记录
        # 向redis追加数据
        # 如果超过数量，多余的数据进行截断
        redis_conn = get_redis_connection('history')
        pl = redis_conn.pipeline()
        # lrem(name, count, value)
        pl.lrem('history_%s' % user_id, 0, sku_id)
        pl.lpush('history_%s' % user_id, sku_id)
        # ltrim(name, start, end)
        pl.ltrim('history_%s' % user_id, 0, constants.USER_BROWSE_HISTORY_LIMIT - 1)

        pl.execute()

        return validated_data


