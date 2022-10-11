import re
from rest_framework import serializers

from .models import User
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username')


class RegisterSerializer(serializers.ModelSerializer):
    def validate_password(self, password):
        if re.fullmatch(r'[A-Za-z0-9_#@!$%^&+=]{8,}', password):
            return password
        else:
            msg = _("Password contains invalid characters or not long enough.")
            raise serializers.ValidationError(msg)

    def create(self, validated_data):
        user = User.objects.create_user(
            **validated_data
        )
        return user
    class Meta:
        model = User
        fields = ('username','password')

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)

    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        required=True
    )

    def authenticate_user(self, user):
        self.user = user
        password = 'X'
        user.set_password(password)
        authenticate(username=user.username, password=user.password)

    def validate(self, attrs):
        username = attrs.get('username', None)

        if username is not None:
            try:
                user = User.objects.get(username=username)
                self.authenticate_user(user)
                if self.user is not None:
                    return attrs
            except:
                pass

        msg = _("Invalid credentials")
        raise serializers.ValidationError(msg)

