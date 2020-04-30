import os
from .base import *

DEBUG = False
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'ssafybook',
        'USER': 'root',
        'PASSWORD': 'ssafyb205',
    }
}