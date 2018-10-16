from django_redis import get_redis_connection
from redis.exceptions import RedisError
from rest_framework import serializers
import logging

logger = logging.getLogger('django')


class CheckImageCodeSerializer(serializers.Serializer):
    """
    图片验证码校验序列化器
    """
    # 基本校验
    image_code_id = serializers.UUIDField()
    text = serializers.CharField(min_length=4, max_length=4)

    # 额外校验逻辑，用于判断图片验证码是否正确
    def validate(self, attrs):
        image_code_id = attrs['image_code_id']
        text = attrs['text']

        redis_conn = get_redis_connection('verify_codes')
        text_server = redis_conn.get('img_%s' % image_code_id)

        if text_server is None:
            # 验证码过期或者不存在
            raise serializers.ValidationError('无效的图片验证码')

        # 删除redis中的图片验证码，防止用户进行多次请求验证
        try:
            # 防止删除图片验证码时产生异常交给exceptions处理造成500错误
            redis_conn.delete('img_%s' % image_code_id)
        except RedisError as e:
            # 一旦产生异常，不做处理
            logger.error(e)

        # 验证码对比
        text_server = text_server.decode()
        if text_server.lower() != text.lower():
            raise serializers.ValidationError('图片验证码错误')

        # redis中发送短信验证码的标志 send_flag_<mobile>:1, 由redis维护60s的有效期
        mobile = self.context['view'].kwargs.get('mobile')
        if mobile:
            send_flag = redis_conn.get('send_flag_%s' % mobile)
            if send_flag:
                raise serializers.ValidationError('发送短信次数过于频繁')
        return attrs
