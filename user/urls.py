from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path
from .views import Profile, Login, MockView, SignUp

from user import views

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("mock/", MockView.as_view(), name="test"),
    path("profile/<int:user_id>/", Profile.as_view(), name="profile"),
    path("login/", Login.as_view(), name="login"),
    path("signup/", SignUp.as_view(), name="signup"),

    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('liked_book/<int:user_id>/', views.LikedBookView.as_view(), name='liked_book_view'),

]
