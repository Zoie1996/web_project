from celery import Celery


# 设置celery使用django配置文件
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'meiduo.settings.dev'

celery_app = Celery('meiduo')

# 导入celery配置(meiduo.celery_tasks.config)
celery_app.config_from_object('celery_tasks.config')

# 自动注册celery任务
celery_app.autodiscover_tasks(['celery_tasks.sms',  # 自动从celery_tasks下的sms中找到tasks文件
                               'celery_tasks.emails',
                               'celery_tasks.html'
                               ])
