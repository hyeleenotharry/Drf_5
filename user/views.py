from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework import status
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
    UserCreateSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.renderers import TemplateHTMLRenderer
from .models import User
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions, generics
from django.shortcuts import redirect, render


# Create your views here.


class Home(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect("book/tag/")
        else:
            return redirect("user/login/")


class SignUp(APIView):
    def get(self, request):
        return render(request, template_name="signup.html")

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "저장 완료"}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
        )


class Login(APIView):
    def get(self, request):
        return render(request, template_name="login.html")


class CustomTokenObtainPairView(TokenObtainPairView):
    # serializer 의 토큰을 커스텀한 토큰키로 봐꿔준다
    # The serializer class that should be used for validating and deserializing input, and for serializing output
    serializer_class = CustomTokenObtainPairSerializer


class MockView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    # 유효한 사용자라면
    def get(self, request):
        # print(request.user)
        user = get_object_or_404(User, email=request.user)
        serializer = UserSerializer(user)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Profile(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        serializer = UserSerializer(user)
        context = {
            "user_data": serializer.data,
        }
        print(user)
        return Response(
            context,
            status=status.HTTP_200_OK,
            template_name="profile.html",
        )

    def put(self, request, user_id):
        if request.user.is_authenticated:
            me = get_object_or_404(User, id=user_id)
            if me == request.user:
                serializer = UserSerializer(me, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("수정 완료", status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
