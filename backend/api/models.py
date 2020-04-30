from django.utils import timezone
from django.db import models
from django.conf import settings
from django.db.models import Avg


class Author(models.Model):
    name = models.CharField(max_length=100)
    imgUrl = models.CharField(max_length=300)
    boneDate = models.CharField(max_length=100, blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField()

class MainCategory(models.Model):
    name = models.CharField(max_length=100)

class SubCategory(models.Model):
    name = models.CharField(max_length=100)
    main = models.ForeignKey(MainCategory,on_delete=models.CASCADE)
    book_category = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favoriteCategory',
        blank=True
    )
    
class DetailCategory(models.Model):
    name = models.CharField(max_length=100)
    sub = models.ForeignKey(SubCategory, on_delete =models.CASCADE)
    
class Book(models.Model):
    isbn = models.CharField(max_length=15, null=True)
    title = models.CharField(max_length=140)
    description = models.TextField()
    priceStandard = models.CharField(max_length=10)
    coverSmallUrl = models.CharField(max_length=150)
    coverLargeUrl = models.CharField(max_length=150)
    publisher = models.CharField(max_length=30)
    translator = models.CharField(max_length=30)
    author = models.ManyToManyField(Author,related_name="author_books",blank=True)
    pubDate = models.CharField(max_length=10)
    contents = models.TextField()
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_books', blank=True)
    mainCategory = models.ForeignKey(MainCategory,on_delete=models.CASCADE, null=True)
    subCategory = models.ForeignKey(SubCategory, on_delete =models.CASCADE, null=True)
    detailCategory = models.ForeignKey(DetailCategory, on_delete=models.CASCADE, null=True)
    publisherReview = models.TextField(null=True)
    r_cnt = models.IntegerField(default=0)
    r_score = models.IntegerField(default=0)
    @property
    def avg(self):
        if self.r_cnt:
            avg = round(self.r_score/self.r_cnt,1)
        else:
            avg = 0
        return avg
    @property
    def categorylist(self):
        return [self.mainCategory.name, self.subCategory.name, self.detailCategory.name if self.detailCategory != None else '']

class Review(models.Model):
    content = models.CharField(max_length=140, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    spoiler = models.BooleanField(default=False)
    like_user = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews', blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)