import os
from celery import Celery


# переменная окружения "DJANGO_SETTINGS_MODULE"
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'store.settings')

# экземпляр объекта Celery
app = Celery('store')

# настройки проекта в Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение и регистрация задач из файлов tasks.py в приложениях Django
app.autodiscover_tasks()

