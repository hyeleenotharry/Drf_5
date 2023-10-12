from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from user.models import User
from .serializers import (
    UserSerializer,
    CustomTokenObtainPairSerializer,
)
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your views here.
class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "저장 완료"}, status=status.HTTP_201_CREATED)
        return Response(
            {"message": f"${serializer.errors}"}, status=status.HTTP_400_BAD_REQUEST
        )

class FollowView(APIView):
    def post(self, request, user_id):
        you = get_object_or_404(User, id=user_id)
        me = request.user
        if me in you.followee.all():
            you.followee.remove(me)
            return Response("unfollow했습니다.", status=status.HTTP_200_OK)
        else:
            you.followee.add(me)
            return Response("follow했습니다.", status=status.HTTP_200_OK)

class CustomTokenObtainPairView(TokenObtainPairView):
    # serializer 의 토큰을 커스텀한 토큰키로 봐꿔준다
    # The serializer class that should be used for validating and deserializing input, and for serializing output
    serializer_class = CustomTokenObtainPairSerializer
