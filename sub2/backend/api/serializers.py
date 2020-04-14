from .models import Store, Book, Category, Review
from rest_framework import serializers


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
    class Meta:
        model = Review
        fields = '__all__'
