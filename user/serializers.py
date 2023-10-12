from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from book.serializers import BookSerializer
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        # set password 로 해싱을 해줘야함
        user.set_password(password)
        print(user.is_active)
        user.save()

        return user

    def update(self, validated_data):
        user = super().create(validated_data)
        password = user.password
        # set password 로 해싱을 해줘야함
        user.set_password(password)
        user.save()

        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        # ...

        return token

class LikedBookSerializer(serializers.ModelSerializer):
    liked_books = BookSerializer(many=True)

    class Meta:
        model = User
        field = ("liked_books",)