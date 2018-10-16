import random

from django.http import HttpResponse
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from celery_tasks.sms.tasks import send_sms_code
from meiduo.libs.captcha.captcha import captcha
from users.models import User
from verifications import serializers
from . import constants


# Create your views here.


# GET /image_codes/<image_code_id>/
# 传入image_code_id，返回图片文件


class ImageCodeView(APIView):
    """
    图片验证码
    """

    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        # 获取redis的链接对象
        redis_conn = get_redis_connection('verify_codes')
        redis_conn.setex('img_%s' % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRE, text)

        return HttpResponse(image, content_type='image/ipg')


#  GET /sms_codes/<mobile>/?image_code_id=xxx&text=xxx
class SMSCodeView(GenericAPIView):
    serializer_class = serializers.CheckImageCodeSerializer

    def get(self, request: Request, mobile):
        # 校验图片验证码和发送短信的频次
        # mobile是被放到了类视图对象中，只要不是查询字符串和请求体，都是存放在view的kwargs属性中
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # 校验通过，生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 保存验证码以及发送记录
        redis_conn = get_redis_connection('verify_codes')
        # redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # redis_conn.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)

        # 使用redis的pipeline管道一次执行多个redis命令
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        # 让管道执行命令
        pl.execute()

        # 发送短信(交给celery异步执行耗时任务)
        # ccp = CCP()
        # ccp.send_template_sms(mobile, [sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60], constants.SMS_CODE_TEMP_ID)

        # 使用celery发布异步任务
        send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'OK'})


class SMSCodeByTokenView(APIView):
    """
    根据access_token发送短信
    """
    def get(self, request: Request):
        # 获取并校验access_token
        access_token = request.query_params.get('access_token')
        if not access_token:
            return Response({'message': '缺少access_token'}, status=status.HTTP_400_BAD_REQUEST)

        # 从access_token中获取手机号
        mobile = User.check_send_sms_code_token(access_token)
        if not mobile:
            return Response({'message': '无效的access_token'}, status=status.HTTP_400_BAD_REQUEST)

        # 判断手机号发送频次
        redis_conn = get_redis_connection('verify_codes')
        send_flag = redis_conn.get('send_flag_%s' % mobile)
        if send_flag:
            return Response({'message': '发送短信次数过于频繁'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # 生成短信验证码
        sms_code = '%06d' % random.randint(0, 999999)

        # 保存并发送短信验证码
        pl = redis_conn.pipeline()
        pl.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.setex('send_flag_%s' % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
        pl.execute()

        send_sms_code.delay(mobile, sms_code)

        return Response({'message': 'OK'})
