from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer, UserUpdatePasswordSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Sum
from django.core.mail import EmailMessage
import string
import random
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
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    elif request.method == 'DELETE':
        user.delete()
        return Response({'message':'deleted!'})

@api_view(['POST'])
def find_password(request):
    Len = 12
    string_pool = string.ascii_letters + string.digits
    result = ''
    for _ in range(Len):
        result += random.choice(string_pool)

    user = get_object_or_404(User, username=request.data.get('username'))
    if user.username == request.data.get('username') and user.email == request.data.get('email'):
        user.password = result
        user.set_password(user.password)
        user.save()
        template = f'''
        비밀번호 재생성을 위해 임시 비밀번호를 발급해드렸습니다.
        비밀번호 : '{result}' 를 입력해주세요.
        '''
        mail = EmailMessage(
            'Book U Love 임시비밀번호 발급', # 제목
            template, # 내용
            to=[f'{user.email}'], # 받을 주소
        )
        # 메일 보내기
        mail.send()
        
        return Response({'message': '메일을 성공적으로 보냈습니다.'})
    else:
        return Response(EOFError)


@api_view(['PUT'])
def password_update(request, id):
    user = get_object_or_404(User, id=id)
    user.password = request.data.get('password')
    serializer = UserUpdatePasswordSerializer(data=request.data, instance=user)
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'message': '비밀번호 변경이 성공적으로 완료되었습니다.'})


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