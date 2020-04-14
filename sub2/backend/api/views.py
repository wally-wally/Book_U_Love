from api import models, serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import render, get_object_or_404
from django.conf import settings


class SmallPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        queryset = (models.Category.objects.all())
        return queryset

class BookViewSet(viewsets.ModelViewSet):
    permission_class = [IsAuthenticated]
    serializer_class = serializers.BookSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        book = models.Book.objects.all()
        id = self.request.query_params.get("id","")
        if id:
            book = book.filter(id=id)

        category = self.request.query_params.get("category","")
        print(category)
        if category:
            print(int(category)%100)
            if int(category) % 100:
                print('here')
                book = book.filter(category_id=category)
            else:
                print('여긴 아니야')
                book = book.filter(category_id__gt=category).filter(category_id__lt=int(category)+100)
        # query = 저자와 
        query = self.request.query_params.get("query","")
        if query:
            book = book.filter(author__contains=query) | book.filter(title__contains=query)

        queryset = (
            book
        )
        return queryset

@api_view(['GET','POST','DEL','PUT'])
def review(request,id):
    book= get_object_or_404(models.Book, id=id)
    print(book)
    if request.method == 'GET':
        serializer = serializers.ReviewSerializer(review, many=True, context={'request': request})
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data
        data["book"] = book
        data["user"] = settings.AUTH_USER_MODEL.objects.get(id=1)
        print(data)
        serializer = serializers.ReviewSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

@api_view(['POST'])
def review_create(request, book_pk):
    # review = request.data
    # print(review)
    serializer = serializers.ReviewSerializer(data=request.data)
    print('serializer', serializer)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data)

@api_view(['GET', 'POST','PUT','DELETE'])
def review_command(request, book_pk, review_pk):
    if request.method == 'GET':
        reviews = models.Review.objects.filter(book=book_pk).order_by('-pk')
        # print(reviews)
        serializer = serializers.ReviewSerializer(reviews, many=True, context={'request': request})
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = serializers.ReviewSerializer(data=request.data)
        # print('serializer', serializer)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

    elif request.method == 'PUT':
        review = get_object_or_404(models.Review, pk=review_pk)
        serializer = serializers.ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'updated competition!!!'})
    else:
        review = get_object_or_404(models.Review, pk=review_pk)
        review.delete()
        return Response({'message':'deleted!!'})
