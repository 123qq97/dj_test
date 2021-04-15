import time
from celery import shared_task

@shared_task
def test():
    print('等待前...')
    time.sleep(5)
    print('等待后...')
