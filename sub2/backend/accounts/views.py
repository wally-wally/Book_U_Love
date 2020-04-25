from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Sum
# Create your views here.
from api.models import Book, MainCategory
from django.http import JsonResponse
from api.serializers import BookSerializer

@api_view(['POST'])
def signup(request):
    error = UserSerializer.validate(get_user_model(), data=request.data)
    if error['password'] or error['username'] or error['email']:
        return Response(error, status=400)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = UserSerializer.create(get_user_model(), request.data)
        serializer = UserSerializer(user)
        return Response(serializer.data)

@api_view(['GET', 'PUT', 'DELETE'])
def user(request):
    user = request.user
    if request.method == 'GET':
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        data = request.data
        serializer = UserUpdateSerializer(data=data, instance=user)
        # print('serializer', serializer)
        if serializer.is_valid(raise_exception=True):
            # print('request.data: ', request.data)
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message':'deleted!'})

from math import sqrt
@api_view(['GET'])
def recommend(request):
    user = request.user
    users = User.objects.all()
    mybook = Book.objects.filter(review__user=user)
    pearson ={}
    cos = {}
    for other in users:
        X,Y, XX,YY,XY,cnt = 0,0,0,0,0,0
        if other != user:
            same_books = mybook.filter(review__user=other)
            for book in same_books:
                a = book.review_set.filter(user=user)[0].score
                b = book.review_set.filter(user=other)[0].score
                X += a
                Y += b
                XX += a*a
                YY += b*b
                XY += a*b
                cnt += 1
            try:
                cos[other.id] = XY/(sqrt(XX) * sqrt(YY))
                pearson[other] = (XY-(X*Y)/cnt)/ sqrt((XX-(X*X)/cnt) * (YY-(Y*Y)/cnt))
            except:
                pass
    sorted_pearson = sorted(pearson.items(), key=lambda kv: kv[1],reverse=True)
    otherUserReview = None
    for pearson in sorted_pearson[:2]:
        user = pearson[0]
        if otherUserReview:
            otherUserReview = otherUserReview | user.review_set.all()
        else:
            otherUserReview = user.review_set.all()
    if otherUserReview:
        recommend = otherUserReview.values('book').annotate(Avg('score')).annotate(Count('score')).annotate(Sum('score'))
        print(recommend)
        print('총 ', len(otherUserReview),'개에서 - ', len(recommend),'개')
        bookdata = []
        for book in recommend.order_by('-score__avg'):
            bookdata.append(book['book'])
        recommend_bookdata = Book.objects.filter(id__in=bookdata).difference(mybook)
        print(recommend_bookdata)
        serializer = BookSerializer(recommend_bookdata,many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'비교할 유저가 없네요'})