from .models import Book, Category, Review
from rest_framework import serializers
from django.contrib.auth import get_user_model

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id','isbn','title','description','priceStandard','coverSmallUrl','coverLargeUrl','category','publisher','author','translator','pubDate','contents','avg','review_cnt','categoryname','like_user']

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

class MyReviewSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    class Meta:
        model = Review
        fields = ('id','content','score','book')

class BookDetailSerializer(serializers.ModelSerializer):
    review_set = ReviewSerializer(many=True)
    my = serializers.SerializerMethodField()
    class Meta(BookSerializer.Meta):
        fields = BookSerializer.Meta.fields + ['review_set','my']

    def get_my(self,obj):
        try:
            user = self.context['request'].user
            myreview = obj.like_user.filter(id=user.id)
            return True if myreview else False
        except:
            return False
class LikeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Book
        field = '__all__'