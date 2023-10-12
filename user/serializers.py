from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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

    def update(self, instance, validated_data):
        instance.email = validated_data["email"]
        instance.username = validated_data["username"]
        instance.nickname = validated_data["nickname"]
        password = validated_data["password"]
        # set password 로 해싱을 해줘야함
        instance.set_password(password)
        instance.save()

        return instance


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        # ...

        return token
