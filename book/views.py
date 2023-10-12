from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from .models import Book, Review, Author, TaggableManager
from .serializers import (
    BookSerializer,
    ReviewSerializer,
    BookTagSerializer,
    ReviewCreateSerializer,
    TagSerializer,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.views.generic import TemplateView, ListView
from taggit.models import Tag
from django.db.models import Count


# Create your views here.
class Main(APIView):
    def get(self, request):
        # 추천 책
        books = (
            Book.objects.all()
            .annotate(likes_cnt=Count("likes"))
            .order_by("likes_cnt")
            .distinct()
            .values()[:4]
        )

        # values() 를 했기 때문에 값이 그대로 전달되지 않음 > serializerMethod 를 추가
        serializer = BookSerializer(books, many=True)

        # 인기 리뷰
        reviews = (
            Review.objects.all()
            .annotate(likes_cnt=Count("likes"))
            .order_by("likes_cnt")
            .values()[:3]
        )

        re_serializer = ReviewSerializer(reviews, many=True)

        # 태그
        tags = Tag.objects.all()
        # print(tags)
        tag_serializer = TagSerializer(tags, many=True)

        serializer_list = [serializer.data, re_serializer.data, tag_serializer.data]

        content = {
            "status": 1,
            "responseCode": status.HTTP_200_OK,
            "data": serializer_list,
        }

        return Response(content)


class CategoryDetail(APIView):
    def get(self, request, category_id):
        books = Book.objects.filter(category_id=category_id).values()
        print(books)
        serializer = BookSerializer(books, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class BookDetail(APIView):
    def get(self, request, book_id):
        book = get_object_or_404(Book, id=book_id)
        serializer = BookTagSerializer(book)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewCreate(APIView):
    def post(self, request, book_id):
        if request.user.is_authenticated:
            serializer = ReviewCreateSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, book_id=book_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("로그인 해주십시오", status=status.HTTP_403_FORBIDDEN)


class ReviewUpdate(APIView):
    def put(self, request, book_id, review_id):
        if request.user.is_authenticated:
            my_review = get_object_or_404(Review, id=review_id)
            if my_review.author == request.user:
                serializer = ReviewCreateSerializer(my_review, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response("수정 완료", status=status.HTTP_200_OK)
                else:
                    return Response(
                        serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)

    def delete(self, request, book_id, review_id):
        my_review = get_object_or_404(Review, id=review_id)
        if my_review.author == request.user:
            my_review.delete()
            return Response("삭제 완료", status=status.HTTP_200_OK)
        else:
            return Response("권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)


# html로 태그 전달
class TagCloudTV(TemplateView):
    # 모든 태그 추출
    template_name = "taggit/tag_cloud_view.html"


class TaggedObjectLV(ListView):
    # 특정 태그가 있는 책들
    template_name = "taggit/tag_with_book.html"
    model = Book

    def get_queryset(self):
        return Book.objects.filter(tags__name=self.kwargs.get("tags"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tags"] = self.kwargs["tags"]
        return context
