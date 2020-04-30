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

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        review = models.Review.objects.all()
        id = self.request.query_params.get("id","")
        if id:
            review = review.filter(user=id)
        queryset = (review)
        return queryset

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    permission_class = [IsAuthenticated]

    def get_queryset(self):
        queryset = (models.MainCategory.objects.all())
        return queryset

class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AuthorSerializer
    pagination_class = SmallPagination
    def get_queryset(self):
        author = models.Author.objects.all()
        return (author)

class BookViewSet(viewsets.ModelViewSet):
    permission_class = [IsAuthenticated]
    serializer_class = serializers.BookSerializer
    pagination_class = SmallPagination

    def get_queryset(self):
        book = models.Book.objects.all()
        id = self.request.query_params.get("id","")
        if id:
            book = book.filter(id=id)
        maincategory = self.request.query_params.get("maincategory","")
        if maincategory:
            book = book.filter(mainCategory_id=maincategory)
        subcategory = self.request.query_params.get("subcategory","")
        if subcategory:
            book = book.filter(subCategory_id=subcategory)
        detailcategory = self.request.query_params.get("detailcategory","")
        if detailcategory:
            book = book.filter(detailCategory_id=detailcategory)
        query = self.request.query_params.get("query","")
        if query:
            book = book.filter(author__name__contains=query).union(book.filter(title__contains=query))
        author = self.request.query_params.get("author","")
        if author:
            book = book.filter(author__id=author)
        sortby = self.request.query_params.get("sortby","")
        if sortby=="count":
            book = sorted(book, key=lambda t: (t.r_cnt,t.avg),reverse=True)
        elif sortby == "score":
            book= sorted(book, key=lambda t: (t.avg,t.r_cnt),reverse=True)
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

        
@api_view(['GET','POST'])
def review_create(request):
    if request.method == 'GET':
        review = models.Review.objects.all()
        serializer = serializers.ReviewSerializer(review, many=True)
        return Response(serializer.data)
    else:
        serializer = serializers.ReviewSerializer(data=request.data)
        book = models.Book.objects.get(id=request.data['book'])
        print(book)
        book.r_score += int(request.data['score'])
        book.r_cnt += 1
        book.save()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data)

@api_view(['PUT','DELETE'])
def review_command(request,review_pk):
    if request.method == 'PUT':
        review = get_object_or_404(models.Review, pk=review_pk)
        serializer = serializers.ReviewSerializer(data=request.data, instance=review)
        book = models.Book.objects.get(id=review.book_id)
        book.r_score -=  review.score - int(request.data['score'])
        book.save()
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':'updated competition!!!'})
    else:
        print('delete_review')
        review = get_object_or_404(models.Review, pk=review_pk)
        book = models.Book.objects.get(id=review.book_id)
        book.r_cnt -= 1
        book.r_score -= review.score
        book.save()
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

    
class LikeCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MyMainCategorySerializer
    def get_queryset(self):
        main = self.request.user.review_set.values('book__mainCategory').annotate(Count('book__mainCategory')).order_by('-book__mainCategory__count')
        mainlist = []
        for m in main[:10]:
            mainlist.append(m['book__mainCategory'])
        mycategory = models.MainCategory.objects.filter(id__in=mainlist)
        queryset = (mycategory)
        return queryset
