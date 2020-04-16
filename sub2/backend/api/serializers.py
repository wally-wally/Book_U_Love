from .models import Book, Category, Review
from rest_framework import serializers
from django.contrib.auth import get_user_model

class BookSerializer(serializers.ModelSerializer):
    categoryname = serializers.SerializerMethodField()
    review_cnt = serializers.SerializerMethodField()
    avg_score = serializers.SerializerMethodField()
    class Meta:
        model = Book
        fields = '__all__'

    def get_categoryname(self,obj):
        category = Category.objects.get(id=obj.category_id)
        return category.name

    def get_review_cnt(self,obj):
        count = Review.objects.filter(book_id=obj.id).count()
        return count

    def get_avg_score(self,obj):
        review = Review.objects.filter(book_id=obj.id)
        if review:
            avg = sum(map(lambda x:x.score,review))/review.count()
        else:
            avg = 0
        return avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    class Meta:
        model = Review
        fields = '__all__'

    def get_username(self,obj):
        user = get_user_model().objects.get(id=obj.user_id)
        return user.username