from django.shortcuts import render
from rest_framework.exceptions import ValidationError
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from users import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from users.models import User
from users.serializers import RegisterSerializer
from users.services import token
from rest_framework import status, generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.services import authentication as authentication_service

from users.services.registration import is_username_used


# Create your views here.
class TokenRefreshView(APIView):
    def get_token(self):
        return self.token


    def get_user(self):
        return self.user

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh", None)

        if refresh_token is None:
            raise Exception(("No refresh token has been provided.",))

        access = token.TokenManager.generate_access(refresh=refresh_token)
        self.token = access

        valid_token = JWTAuthentication().get_validated_token(raw_token=self.token)
        self.user = JWTAuthentication().get_user(validated_token=valid_token)

        return Response({'access': access}, status=status.HTTP_200_OK)


class Login(APIView):
    serializer_class = serializers.LoginSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_token(self):
        return self.token

    def get_user(self):
        if hasattr(self, '_user') and User.objects.filter(id=self._user.id).exists():
            return self._user
        self._user = get_object_or_404(User, id=self.request.user.id)
        return self._user

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._user = serializer.data['user']
        self.request.user = self._user
        refresh, access = token.TokenManager.generate_refresh_token(user=self.get_user())
        data = {
            'access': access,
            'refresh': refresh,
            'phone_number': self.get_user().phone_number_str,
            'email': self.get_user().email
        }
        self.token = data['access']
        data['next'] = self.get_next_step()

        response = Response(data, status=status.HTTP_200_OK)
        return response


class Register(generics.CreateAPIView):
    serializer_class = serializers.RegisterSerializer

    def get_serializer_class(self):
        return self.serializer_class

    def get_token(self):
        return self.token

    def get_user(self):
        if hasattr(self, '_user') and User.objects.filter(id=self._user.id).exists():
            return self._user
        self._user = get_object_or_404(User, id=self.request.user.id)
        return self._user

    def get_serializer_context(self):
        data = super().get_serializer_context()
        return data

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # raise Exception(serializer.validated_data['username'])

        username = serializer.validated_data['username']

        if is_username_used(username):
            raise ValidationError({
                'username':
                    _("someone already registered with given username")
            })

        user = User()
        user.username = user.username
        user.save()
        refresh, access = self.token.TokenManager.generate_refresh_token(user=self.get_user())
        data = {
            'access': access,
            'refresh': refresh,
            'phone_number': self.get_user().phone_number_str,
            'email': self.get_user().email
        }
        self.token = data['access']

        return Response(data={
            'auth_token': token,
        }, status=HTTP_201_CREATED)
