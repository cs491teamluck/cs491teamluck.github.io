from django.shortcuts import render
from django.http import HttpResponse
from rythm.models import *
from rythm.serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
import datetime



# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class SignupView(APIView):
    def post(self, request):
        user = UserSerializer(data=request.data)
        if user.is_valid():
            user.save()
            return Response(user.data)
        return Response(user.errors)

class LoginView(APIView):
    def post(self, request):
        user = User.objects.filter(email=request.data['email'], password=request.data['password']).first()
        if user:
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response("Login not successful")
class SeeUsersView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


