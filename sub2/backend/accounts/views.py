from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
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