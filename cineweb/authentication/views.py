from django.shortcuts import render

from rest_framework.views import APIView

from rest_framework.response import Response

from django.contrib.auth import authenticate,login

from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        user_data = request.data

        username = user_data.get('username')

        password = user_data.get('password')

        user = authenticate(username=username,password=password)

        if user :

            refresh = RefreshToken.for_user(user)

            access = refresh.access_token

            data = {'access':str(access),'refresh':str(refresh)}

            return Response(data)
    
        data = {'msg':'invalid username and password'}

        return Response(data)