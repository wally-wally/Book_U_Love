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
from datetime import datetime, timedelta

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
        categorypage = self.request.query_params.get("categorypage","")
        if sortby:
            if not categorypage:
                book = book.filter(r_cnt__gt=0)
        if sortby=="count":
            book = sorted(book, key=lambda t: (t.r_cnt,t.avg),reverse=True)
        elif sortby == "score":
            if not categorypage:
                books = models.Book.objects.filter(r_cnt__gte=3)
                book= sorted(books, key=lambda t: (t.avg,t.r_cnt),reverse=True)
            else:
                book= sorted(book, key=lambda t: (t.avg,t.r_cnt),reverse=True)
        top = self.request.query_params.get("top","")
        if top:
            book = book[:int(top)]
        other_books = self.request.query_params.get("other_books", "")
        if other_books:
            sub_id = models.Book.objects.get(id=other_books).subCategory_id
            book = models.Book.objects.filter(subCategory_id=sub_id).order_by('-r_score', 'r_cnt')
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

class AllCategoryReview(viewsets.ModelViewSet):
    serializer_class = serializers.TotalmainCategorySerializer
    def get_queryset(self):
        review = models.MainCategory.objects.all()
        return review

@api_view(['GET'])
def categoryfilter(request):
    review = models.Review.objects.all()
    age = request.query_params.get('age','')
    if age:
        review = review.filter(user__age__startswith=int(age)//10)
    qgender = request.query_params.get('gender','')
    if qgender:
        gender = 'M' if qgender == '남자' else 'F'
        review = review.filter(user__gender=gender)
    review = review.values('book__detailCategory__name','book__detailCategory').annotate(Count('id')).order_by('-id__count')
    return Response(review)

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


## 나이, 성별 분류별 카테고리
@api_view(['GET'])
def review_age(request):
    ## 중복되는 isbn 책이 있음
    # book = models.Book.objects.values('isbn').annotate(Count('id')).filter(id__count__gt=1)
    # print(len(book))
    # for i in book:
        # print(models.Book.objects.filter(isbn=i['isbn'])[0].title)

    review = models.Review.objects.filter(user__age__startswith="2")
    review = review.filter(user__gender="M")
    # print(review)
    return Response(list(review))


@api_view(['POST'])
def review_like(request):
    data = request.data
    review = get_object_or_404(models.Review, pk=data['review'])
    user = get_object_or_404(get_user_model(),pk=data["user"])
    if user not in review.like_user.all():
        review.like_user.add(user)
        is_liked = True
    else:
        review.like_user.remove(user)
        is_liked = False
    return JsonResponse({'is_liked':is_liked,'like_count':review.like_user.count()})
# 책을 가져오는데 최근(일주일)에 리뷰가 많이 달린 순으로
# 책마다 r_cnt로 비교
# 리뷰를 가져와서 datetime(today)-created_at

# datetime.strptime('2020-04-30T20:41:36.086052+09:00'[:10], '%Y-%m-%d')-datetime.now()
@api_view(['GET'])
def review_orderby_date(request):
    reviews = models.Review.objects.all().filter(created_at__gte=datetime.now()-timedelta(days=7))
    review = reviews.values('book_id').annotate(Count('id')).order_by('-id__count')
    print(review)
    books = []
    for a in review[:10]:
        serializer = serializers.BookDetailSerializer(models.Book.objects.get(id=a['book_id']))
        books.append((serializer.data,a['id__count']))
    return Response(books)


@api_view(['GET'])
def bookfilter(request):
    review = models.Review.objects.all()
    review = models.Review.objects.all()
    age = request.query_params.get('age','')
    if age:
        review = review.filter(user__age__startswith=int(age)//10)
    qgender = request.query_params.get('gender','')
    if qgender:
        gender = 'M' if qgender == '남자' else 'F'
        review = review.filter(user__gender=gender)
    review = review.values('book__id').annotate(Count('id')).order_by('-id__count')
    books = []
    for a in review[:10]:
        serializer = serializers.BookDetailSerializer(models.Book.objects.get(id=a['book__id']))
        books.append((serializer.data,a['id__count']))
    return Response(books)


@api_view(['GET'])
def filter_by_score_and_count(request):
    print(request.data)
    books = models.Book.objects.all()
    maincategory = request.data.get("maincategory","")
    if maincategory:
        books = books.filter(mainCategory_id=maincategory)
    subcategory = request.data.get("subcategory","")
    if subcategory:
        books = books.filter(subCategory_id=subcategory)
    detailcategory = request.data.get("detailcategory","")
    if detailcategory:
        books = books.filter(detailCategory_id=detailcategory)

    cnt = request.data.get('r_cnt', '')
    print('cnt', cnt)
    if cnt:
        books = books.filter(r_cnt__gte=int(cnt))
    score = request.data.get('r_score', '')
    print('score', score)
    if score:
        books = books.filter(r_score__gte=int(score)/int(cnt))
    book = books.values('id', 'title', 'r_cnt', 'r_score', 'mainCategory', 'subCategory', 'detailCategory')
    print('cnt here')

    print(book[:10])
    return Response(book)