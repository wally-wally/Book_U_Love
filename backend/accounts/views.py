from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .serializers import UserSerializer, UserUpdateSerializer, UserDetailSerializer, UserUpdatePasswordSerializer, UserSimpleSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count, Sum
from django.core.mail import EmailMessage
import string
import numpy as np
from faker import Faker
from api.models import SubCategory, Book, Review
import random
# Create your views here.
from api.models import Book, MainCategory
from django.http import JsonResponse
from api.serializers import BookSerializer

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSimpleSerializer
    def get_queryset(self):
        queryset = (User.objects.all())
        return queryset

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

@api_view(['POST'])
def createuser(request):
    contents = {
        10 : ['재밌게 읽었습니다', '책 피고 그자리에서 다 읽어버렸네요\n재밌어요 !', '아주 좋은 책! 추천합니다','이 작가님의 다음 책이 기대가 되는 군요','완벽.. 전개와 결말이 완벽했습니다','등장인물의 묘사와 디테일한 감정선\n폭풍처럼 몰아치는 전개와 극적인 결말\n제가 본 책중 Best입니다','와 이책을 지금 읽은게 후회가 되는군요'],
        9 : ['재밌는 책입니다','제가 좋아하는 작가님 ! 표현력이 좋아요','두 번째 읽는데 재미있어요','도움이 많이 되는 책입니다','꿀재앰'],
        8: ['읽다보니 시간이 벌써 이렇게 갔네요','엄청 재밌어요','좋아요 ! 또 읽을 예정입니다','잼','8점정도가 적당한 책인것 같네요','지인에게 추천해줬는데 잘 읽었다고 합니다'],
        7: ['읽을만 합니다','추천 ! 좋은 책이에요','재밌게 읽었네요', '결말이 조금 아쉬운데 재미있었네요','나름 재미있네요','시간날 때 읽기 좋아요'],
        6 : ['재밌었습니다','전개가 조금 아쉽긴 하지만 전체적으로 재미있었어요','이 작가님은 제가 많이 좋아해서 기대했는데 쪼금 아쉽네요','열심히 읽었어요','열심히 읽었어요',],
        5 : ['아 기대많이 했는데 좀 아쉽네요','저랑은 좀 안맞는거 같아요 다른사람들은 재밌다 그럤는데..','시간떼우기 좋은 책이네요','흐음..','딱 5점정도..'],
        4: ['그닥..','이거 전개가 왜이러죠','제목이 재밌어보였는데.. 흠',''],
        3: ['노오재앰','이게 무슨내용이지','재미없군..','싫어하는 사람에게 선물하세요','안읽히네요 ㅜㅜ노잼'],
        2: ['이게뭐야','완전 재미없어요','우엑','나도 작가하겠다','한 10장보고 접었네요'],
        1: ['이 책은 뗄감으로 쓰세요','개노잼','11점 주고 싶은 마음으로 1점드립니다','내맘속의 1등이라 1점드립니다']
    }
    spoiler = [True,False,False,False]
    fake = Faker('ko_KR')
    email = fake.email()
    userdata = {
        'username' : fake.name(),
        'email' : email,
        'age' : request.data['age'],
        'gender' : request.data['gender'],
        'password' : 'test!' + email.split('@')[0]
    }
    serializer = UserSerializer(data=userdata)
    if serializer.is_valid(raise_exception=True):
        user= UserSerializer.create(get_user_model(),userdata)
        for c in request.data['categorys']:
            sub = SubCategory.objects.get(id=c)
            user.favoriteCategory.add(sub)
            books = Book.objects.filter(subCategory=sub)
        recommend = set()
        l = len(books)
        for _ in range(int(l ** (1/3)*2 + l//10 -1)):
            s = np.random.normal(0,l//3)
            if s >= l:
                s = 2 * l - s -1
            ss = abs(round(s,0))
            recommend.add(int(ss))
        for r in recommend:
            if r <= 1 //10 :
                score = np.random.normal(8.5,1)+0.2
            elif r <= l //5:
                score = np.random.normal(8.3,1)+0.2
            elif r <= l//2:
                score = np.random.normal(8.0,1.5)
            else:
                score = np.random.normal(7.8,1.5)
            score = int(round(max(min(score,10),1)))
            try:
                review = Review.objects.create(
                    score = score,
                    book = books[r],
                    user = user,
                    content = contents[score][np.random.randint(0,len(contents[score]))],
                    spoiler = spoiler[np.random.randint(0,4)]
                )
                c_month = str(np.random.randint(3,5))
                c_date = str(np.random.randint(1,31))
                review.created_at = '2020-0' + c_month + '-' + c_date + 'T13:30:41.927745+09:00'
                review.save()
                books[r].r_cnt += 1
                books[r].r_score += score
                books[r].save()
            except:
                pass
        other = Book.objects.all()
        ll = len(other)
        other_recommend = set()
        for _ in range(int(l ** (1/3)*2 + l//10 -1)//2):
            s = np.random.normal(0,ll//10)
            if s >= ll:
                s = 2 * ll - s -1
            ss = abs(round(s,0))
            other_recommend.add(int(ss))
        other_recommend -= recommend
        for r in other_recommend:
            try:
                score = int(round(max(min(np.random.normal(7.0,1.5),10),0))-0.3)
                review = Review.objects.create(
                    score = score,
                    book = other[r],
                    user = user,
                    content = contents[score][np.random.randint(0,len(contents[score]))],
                    spoiler = spoiler[np.random.randint(0,4)]
                )
                c_month = str(np.random.randint(3,5))
                c_date = str(np.random.randint(1,31))
                review.created_at = '2020-0' + c_month + '-' + c_date + 'T13:30:41.927745+09:00'
                review.save()
                other[r].r_cnt += 1
                other[r].r_score += score
                other[r].save()
            except:
                pass
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
        for data in user.favoriteCategory.all():
            user.favoriteCategory.remove(data)
        for c in request.data['categorys']:
            sub = SubCategory.objects.get(id=c)
            user.favoriteCategory.add(sub)
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
    for other in users:
        X,Y, XX,YY,XY,cnt = 0,0,0,0,0,0
        if other != user:
            same_books = mybook.filter(review__user=other)
            if len(same_books) > 5:
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
                    pearson[other] = (XY-(X*Y)/cnt)/ sqrt((XX-(X*X)/cnt) * (YY-(Y*Y)/cnt))
                except:
                    pass
    sorted_pearson = sorted(pearson.items(), key=lambda kv: kv[1],reverse=True)
    print(sorted_pearson)
    otherUserReview = None
    for pearson in sorted_pearson[:1]:
        user = pearson[0]
        if otherUserReview:
            otherUserReview = otherUserReview | user.review_set.all()
        else:
            otherUserReview = user.review_set.all()
    if otherUserReview:
        recommend = otherUserReview.values('book').annotate(Avg('score')).annotate(Count('score')).annotate(Sum('score'))
        bookdata = []
        for book in recommend:
            bookdata.append(book['book'])
        recommend_bookdata = Book.objects.filter(id__in=bookdata).difference(mybook)
        print(recommend_bookdata[:10])
        serializer = BookSerializer(recommend_bookdata[:10],many=True)
        return Response(serializer.data)
    else:
        return Response({'message':'비교할 유저가 없네요'})