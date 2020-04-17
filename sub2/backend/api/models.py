from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models import Avg

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
    @property
    def avg(self):
        avg = self.review_set.aggregate(Avg('score'))['score__avg'] 
        return avg if avg else 0
    @property
    def categoryname(self):
        return Category.objects.get(id=self.category_id).name
    @property
    def review_cnt(self):
        return self.review_set.count()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_books', blank=True)
    
class Review(models.Model):
    content = models.CharField(max_length=140, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)