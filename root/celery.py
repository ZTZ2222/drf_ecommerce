import os
from celery import Celery
from decouple import config

os.environ.setdefault("DJANGO_SETTINGS_MODULE", config("DJANGO_SETTINGS_MODULE"))
app = Celery("root")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
