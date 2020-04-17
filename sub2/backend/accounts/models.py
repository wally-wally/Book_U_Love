from django.db import models
from django.contrib.auth.models import AbstractUser
from api import models as C_model

# Create your models here.
class User(AbstractUser):
    favoriteCategory = models.ManyToManyField(
        C_model.Category,
        related_name='book_category',
        blank=True
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.TextField(null=True)
    gender = models.CharField(max_length=1, null=True)
    age = models.IntegerField(null=True)

