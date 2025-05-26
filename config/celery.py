from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка модуля настроек Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Создание экземпляра приложения Celery
app = Celery('config')

# Загрузка настроек из Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()
