from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from rest_framework import permissions
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import get_user_model ,login
from .serializer import  CreateUserSerializer , LoginSerializer


class ValidateUser(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if username:
            username = str(username)
            user = User.objects.filter(username__iexact=username)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'User name already exists'
                })
            else:
                return Response({
                    'status': True,
                    'detail': 'User name created'
                })
        else:
            return Response({
                    'status': False,
                    'detail': 'pls enter username'
                })


class Register(APIView):
    def post(self, request):
        username = request.data.get('username', False)
        password = request.data.get('password', False)
        if username and password :
            old = User.objects.filter(username__iexact=username)
            if old.exists():
                return Response({
                    "status": False,
                    "detail": "username is already taken"
                })
            else:
                temp_data = {
                    'username': username,
                    'password': password
                }
                serializers = CreateUserSerializer(data=temp_data)
                serializers.is_valid(raise_exception=True)
                serializers.save()
                return Response({
                    "status": True,
                    "detail": "Account is created successfully "
                })
        else:
            return Response({
                "status": False,
                "detail": "phone and password not sent"
            })






class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super().post(request, format=None)
