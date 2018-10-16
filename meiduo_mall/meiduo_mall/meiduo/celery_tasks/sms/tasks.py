from .yuntongxun.sms import CCP
from . import constants
from ..main import celery_app


# 定义异步任务
@celery_app.task(name='sms_code')  # 任务名
def send_sms_code(mobile, sms_code):
    """
    发送短信任务
    :param mobile: 手机号
    :param sms_code: 验证码
    :return: None
    """
    # 发送短信
    ccp = CCP()
    time = constants.SMS_CODE_REDIS_EXPIRES // 60
    ccp.send_template_sms(mobile, [sms_code, time], constants.SMS_CODE_TEMP_ID)

# 开启任务的命令
# celery -A celery_tasks.main worker -l info
