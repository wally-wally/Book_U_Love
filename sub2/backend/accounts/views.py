from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer, UserUpdateSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from .models import User
from django.shortcuts import get_object_or_404
# Create your views here.


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
    print(user)
    if request.method == 'GET':
        serializer = UserUpdateSerializer(user)
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
