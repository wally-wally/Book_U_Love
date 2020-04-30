from .models import Book, Review, MainCategory, SubCategory, DetailCategory, Author
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Avg, Count, Sum

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id','name','imgUrl','boneDate','region','description']

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True,many=True)
    class Meta:
        model = Book
        fields = ['id','isbn','title','description','priceStandard','coverSmallUrl','coverLargeUrl','publisher','translator','pubDate','contents','avg','r_cnt','categorylist','like_user','author', 'publisherReview']

class DetailCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailCategory
        fields = ['id','name']

class subCategorySerializer(serializers.ModelSerializer):
    detailcategory_set = DetailCategorySerializer(many=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name','detailcategory_set']

class CategorySerializer(serializers.ModelSerializer):
    subcategory_set = subCategorySerializer(many=True)
    class Meta:
        model = MainCategory
        fields = ['id','name','subcategory_set']

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
    author = AuthorSerializer(read_only=True,many=True)
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
    # def get_review(self,obj):
    #     myreview = obj.review_set.filter(user=self.context['request'].user)
    #     my_review = ReviewSerializer(myreview)
    #     return my_review
        # other = obj.review_set.filter(user!=self.context['request'].user)

class LikeSerializer(serializers.ModelSerializer):
    class Meta():
        model = Book
        field = '__all__'

class MyDetailCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()
    class Meta:
        model = DetailCategory
        fields = ['name','count','avg']
    def get_count(self,obj):
        review = Review.objects.filter(book__detailCategory=obj).filter(user=self.context['request'].user)
        return len(review)
    def get_avg(self,obj):
        review = Review.objects.filter(book__detailCategory=obj).filter(user=self.context['request'].user).aggregate(Avg('score'))["score__avg"]
        return review


class MysubCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()
    detailcategory_set = MyDetailCategorySerializer(many=True)
    class Meta:
        model = SubCategory
        fields = ['name','count','avg','detailcategory_set']
    def get_count(self,obj):
        review = Review.objects.filter(book__subCategory=obj).filter(user=self.context['request'].user)
        return len(review)
    def get_avg(self,obj):
        review = Review.objects.filter(book__subCategory=obj).filter(user=self.context['request'].user).aggregate(Avg('score'))["score__avg"]
        return review
    
class MyMainCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    avg = serializers.SerializerMethodField()
    subcategory_set = MysubCategorySerializer(many=True)
    class Meta:
        model = MainCategory
        fields = ['name','avg','count','subcategory_set']

    def get_count(self,obj):
        review = Review.objects.filter(book__mainCategory=obj).filter(user=self.context['request'].user)
        return len(review)
    def get_avg(self,obj):
        review = Review.objects.filter(book__mainCategory=obj).filter(user=self.context['request'].user).aggregate(Avg('score'))["score__avg"]
        return review

class TotaldetailCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    class Meta:
        model = DetailCategory
        fields = ['name','count']

    def get_count(self,obj):
        review = Review.objects.filter(book__detailCategory=obj).all()
        return len(review)

class TotalsubCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    detailcategory_set = TotaldetailCategorySerializer(many=True)
    class Meta:
        model = MainCategory
        fields = ['name','count','detailcategory_set']

    def get_count(self,obj):
        review = Review.objects.filter(book__subCategory=obj).all()
        return len(review)

class TotalmainCategorySerializer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    subcategory_set = TotalsubCategorySerializer(many=True)
    class Meta:
        model = MainCategory
        fields = ['name','count','subcategory_set']

    def get_count(self,obj):
        review = Review.objects.filter(book__mainCategory=obj).all()
        return len(review)