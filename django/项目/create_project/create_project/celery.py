import os
from celery import Celery
from django.conf import settings

# 设置celery的环境变量和django-celery的工作目录
os.environ.setdefault('DJANGO_SETTINGS_MODULE','whthas_home.settings')
# 实例化celery应用，传入服务器名称
app = Celery('portal')
# 加载celery配置
app.config_from_object('django.conf:settings')
# 如果在项目中，创建了task.py,那么celery就会沿着app去查找task.py来生成任务
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))