from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.urls import path

from user import views

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('follow/<int:user_id>/', views.FollowView.as_view(), name='follow_view'),
    path('liked_book/<int:user_id>/', views.LikedBookView.as_view(), name='liked_book_view'),
]
