from django.urls import path
from . import views

urlpatterns = [
    path("mainpage/", views.Main().as_view(), name="mainpage"),
    path(
        "mainpage/<int:category_id>/",
        views.CategoryDetail().as_view(),
        name="category-book",
    ),
    path("tag/", views.TagCloudTV.as_view(), name="tag_cloud"),
    path(
        "tag/<str:tags>/",
        views.TaggedObjectLV.as_view(),
        name="tagged_object_list",
    ),
    path("tag/<str:tag>/", views.TaggedObjectLV.as_view(), name="tagged_object_list"),
    path("<int:book_id>/", views.BookDetail.as_view(), name="detail-book"),
    path("<int:book_id>/review/", views.ReviewCreate.as_view(), name="review-create"),
    path(
        "<int:book_id>/review/<int:review_id>/",
        views.ReviewUpdate.as_view(),
        name="review-update",
    ),
]
