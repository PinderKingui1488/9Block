"""
Конфигурация WSGI для проекта config.

Предоставляет WSGI-приложение как переменную уровня модуля с именем ``application``.

Для получения дополнительной информации об этом файле, см.
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
