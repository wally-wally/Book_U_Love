from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
# Create your views here.
from api.models import Book

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
def user(request, id):
    # print(request.data)
    user = get_object_or_404(User, id=id)
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

def user_like(request,id):
    user = User.objects.get(id=id)
    # data = User.objects.get(id=id).review_set.all().values()
    # df = pd.DataFrame(list(data))
    category = user.review_set.values('book__category__name').annotate(Avg('score'))
    category_cnt = user.review_set.values('book__category__name').annotate(Count('score'))
    print(category_cnt)
    print(category)
    # values('book').annotate(Avg('score'))
    #     for genre in review.movie.genres.all():
    #         if genre.name not in user_genres:
    #             user_genres[genre.name] = [0,0]
    #         user_genres[genre.name][0] += review.score
    #         user_genres[genre.name][1] += 1
    # for idx,value in user_genres.items():
    #     user_genres[idx] = [round(value[0]/value[1],2),value[1]]
    # genres = sorted(user_genres.items(),key=lambda x:x[1][0],reverse=True)
    from math import sqrt
    users = User.objects.all()
    mybook = Book.objects.filter(review__user=user)
    vs ={}
    for other in users:
        X,Y, XX,YY,XY,cnt = 0,0,0,0,0,0
        if other != user:
            same_books = mybook.filter(review__user=other)
            print(other)
            for book in same_books:
                # print(book.review_set.values('user','score'))
                a = book.review_set.filter(user=user)[0].score
                b = book.review_set.filter(user=other)[0].score
                print(a,b)
                X += a
                Y += b
                XX += a*a
                YY += b*b
                XY += a*b
                cnt += 1
        print(X,Y, XX, YY, XY, cnt)
        try:
            vs[other] = (XY-(X*Y)/cnt)/ sqrt((XX-(X*X)/cnt) * (YY-(Y*Y)/cnt))
        except:
            pass
    print(vs)
    sorted_vs = sorted(vs.items(), key=lambda kv: kv[1],reverse=True)
    return review