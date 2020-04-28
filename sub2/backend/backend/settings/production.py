import os
from .base import *

DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '127.0.0.1',
        'NAME': 'ssafybook',
        'USER': 'root',
        'PASSWORD': 'ssafyb205',
    }
}