# celery连接配置
broker_url = 'redis://127.0.0.1/14'  # 任务发起者给指定的任务队列(这里用redis做任务队列)
result_backend = 'redis://127.0.0.1/15'  # # 任务执行者从将任务的执行结果保存的位置
