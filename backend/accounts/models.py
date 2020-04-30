from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.TextField(null=True)
    gender = models.CharField(max_length=1, null=True)
    age = models.IntegerField(null=True)