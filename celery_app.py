import celery
import os

CELERY_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')

app = celery.Celery('tasks', 
                    broker = CELERY_URL,
                    include=['tasks']
                    )

app.conf.task_default_queue = 'fetch'