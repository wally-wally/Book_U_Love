from .models import Store, Book, Category, Review
from rest_framework import serializers
from django.contrib.auth import get_user_model

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
        ]

class BookSerializer(serializers.ModelSerializer):
    categoryname = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = '__all__'

    def get_categoryname(self,obj):
        category = Category.objects.get(id=obj.category_id)
        return category.name

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