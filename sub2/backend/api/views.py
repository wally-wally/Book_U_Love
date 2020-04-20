from api import models, serializers
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import get_user_model
from django.db.models import Count,Avg
from django.http import JsonResponse

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
        if category:
            if int(category) % 100:
                book = book.filter(category_id=category)
            else:
                book = book.filter(category_id__gt=category).filter(category_id__lt=int(category)+100)
        query = self.request.query_params.get("query","")
        if query:
            book = book.filter(author__contains=query) | book.filter(title__contains=query)
        sortby = self.request.query_params.get("sortby","")
        if sortby=="count":
            book = sorted(book, key=lambda t: (t.review_cnt,t.avg),reverse=True)
        elif sortby == "score":
            book= sorted(book, key=lambda t: t.avg,reverse=True)
        top = self.request.query_params.get("top","")
        if top:
            book = book[:int(top)]
        queryset = (
            book
        )
        return queryset

class BookDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BookDetailSerializer
    def get_queryset(self):
        book = models.Book.objects.filter(id=self.kwargs['id'])
        queryset = (book)
        return queryset

    def get_my(self):
        book = models.Book.objects.filter(id=self.kwargs['id'])
        if self.request.user.id:
            if self.request.user in book[0].like_user.all():
                a = True
            else:
                a = False
        return a

# @api_view(['GET'])
# def review(request,id):
#     book= get_object_or_404(models.Book, id=id)
#     review = models.Review.objects.filter(book_id=id)
#     serializer = serializers.ReviewSerializer(review, many=True)
#     return Response(serializer.data)

@api_view(['POST'])
def review_create(request):
    serializer = serializers.ReviewSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT','DELETE'])
def review_command(request,review_pk):
    if request.method == 'PUT':
        review = get_object_or_404(models.Review, pk=review_pk)
        serializer = serializers.ReviewSerializer(data=request.data, instance=review)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'updated competition!!!'})
    else:
        print('delete_review')
        review = get_object_or_404(models.Review, pk=review_pk)
        review.delete()
        return Response({'message':'deleted!!'})


# @api_view(['GET'])
# def like_book(request):
#     book = get_object_or_404(models.Book, id=id)
#     if request.method == 'GET':
#         return Response(serializer.data)

@api_view(['POST'])
def like_book(request):
    data = request.data
    book = get_object_or_404(models.Book,pk=data['book'])
    user = get_object_or_404(get_user_model(),pk=data["user"])
    if user not in book.like_user.all():
        book.like_user.add(user)
        is_liked = True
    else:
        book.like_user.remove(user)
        is_liked = False
    return JsonResponse({'is_liked':is_liked,'like_count':book.like_user.count()})

# @api_view(['PUT','DELETE'])
# def like(request):
#     if request.method == 'PUT':
#         review = get_object_or_404(models.Review, pk=review_pk)
#         serializer = serializers.ReviewSerializer(data=request.data, instance=review)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'message':'updated competition!!!'})
#     else:
#         review = get_object_or_404(models.Review, pk=review_pk)
#         review.delete()
#         return Response({'message':'deleted!!'})

@api_view(['GET'])
def mylike(request):
    book = models.Book.objects.filter(like_user=request.user)
    serializer = serializers.BookSerializer(book,many=True)
    return Response(serializer.data)