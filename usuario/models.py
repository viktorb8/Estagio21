from django.db import models

from django.apps import AppConfig

class MyAppConfig(AppConfig):
    default_auto_field = 'django.db.models.AutoField'
    name = 'my_app'

# Create your models here.
