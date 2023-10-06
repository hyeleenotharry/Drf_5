from django.urls import path
from . import views

urlpatterns = [
    path("mainpage/", views.Main().as_view(), name="mainpage"),
    path("book/<int:book_id>/", views.BookDetail.as_view(), name="detail-book"),
    path(
        "book/<int:book_id>/review/", views.ReviewCreate.as_view(), name="review-create"
    ),
    path(
        "book/<int:book_id>/review/<int:review_id>/",
        views.ReviewUpdate.as_view(),
        name="review-update",
    ),
]
