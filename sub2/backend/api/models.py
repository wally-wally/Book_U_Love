from django.utils import timezone
from django.db import models
from django.conf import settings

class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, null=True)
    area = models.CharField(max_length=50, null=True)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=200, null=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []

class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)

class Book(models.Model):
    isbn = models.CharField(max_length=12)
    title = models.CharField(max_length=140)
    description = models.TextField()
    priceStandard = models.CharField(max_length=10)
    coverSmallUrl = models.CharField(max_length=150)
    coverLargeUrl = models.CharField(max_length=150)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    publisher = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    translator = models.CharField(max_length=30)
    pubDate = models.CharField(max_length=10)
    contents = models.TextField()

class Review(models.Model):
    content = models.CharField(max_length=140, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)