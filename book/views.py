from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework.generics import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import status, permissions, generics
from .models import Book, Review, Author, TaggableManager
from user.models import User
from .serializers import (
    BookSerializer,
    ReviewSerializer,
    BookTagSerializer,
    ReviewCreateSerializer,
    TagSerializer,
)
from taggit.serializers import TagListSerializerField, TaggitSerializer
from django.views.generic import TemplateView, ListView
from django.views.generic.detail import DetailView
from taggit.models import Tag
from django.db.models import Count, Aggregate, Avg
from django.forms.models import model_to_dict


# Create your views here.
class Main(APIView):
    def get(self, request):
        print("hello")
        print("this is also test1111~~!!")
        # 추천 책
        books = (
            Book.objects.all()
            .annotate(likes_cnt=Count("likes"))
            .order_by("likes_cnt")
            .distinct()
            .values()[:4]
        )

        print("Test")
        print("Hello World I'm doing great I'm fine thx")

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


class CategoryDetail(ListView):
    template_name = "book_category.html"
    model = Book

    def get_queryset(self):
        return Book.objects.filter(category_id=self.kwargs.get("category_id"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cagegory_id"] = self.kwargs["category_id"]
        return context


class BookDetail(generics.RetrieveAPIView):
    renderer_classes = (TemplateHTMLRenderer,)

    def get(self, request, book_id, *args, **kwargs):
        book = get_object_or_404(Book, id=book_id)
        star_book = Review.objects.filter(book_id=book_id).values()
        i = len(star_book)
        for rv in range(i):
            star = ""
            author_id = star_book[rv]["author_id"]
            author_name = get_object_or_404(User, id=author_id).email
            star_book[rv]["author_id"] = author_name

            star_cnt = star_book[rv]["star"]
            if star_cnt:
                for j in range(star_cnt):
                    star += "⭐"
                star_book[rv]["star"] = star

        review_cnt = len(star_book)
        # print(review_cnt)
        avg_star = int(star_book.aggregate(Avg("star", default=0))["star__avg"])
        # print(avg_star)

        serializer = BookTagSerializer(book)

        context = {
            "book_data": serializer.data,
            "avg_star_range": range(
                avg_star
            ),  # 장고 템플릿에서는 range 를 쓸 수 없기 때문에 미리 range()를 해서 넘겨줘야 함
            "review_cnt": review_cnt,
            "reviews": star_book,
        }

        return Response(
            context,
            status=status.HTTP_200_OK,
            template_name="book_detail.html",
        )


# class BookDetail(ListView):
#     template_name = "book_detail.html"
#     context_object_name = "book_detail_data"

#     def get_queryset(self):
#         book_id = self.kwargs["book_id"]
#         # print(book_id)
#         book = get_object_or_404(Book, id=book_id)
#         print(book)
#         star_book = Review.objects.filter(book_id=book_id).values()
#         i = len(star_book)

#         for rv in range(i):
#             star = ""
#             author_id = star_book[rv]["author_id"]
#             author_name = get_object_or_404(User, id=author_id).email
#             star_book[rv]["author_id"] = author_name

#             star_cnt = star_book[rv]["star"]
#             if star_cnt:
#                 for j in range(star_cnt):
#                     star += "⭐"
#                 star_book[rv]["star"] = star

#         review_cnt = len(star_book)
#         avg_star = int(star_book.aggregate(Avg("star", default=0))["star__avg"])

#         data = {
#             "book_data": book,
#             "avg_star_range": range(avg_star),
#             "review_cnt": review_cnt,
#             "reviews": star_book,
#         }
#         return data

#     def render_to_response(self, context):
#         book = context["book_detail_data"]
#         # print(book)
#         serialized_book = BookSerializer(book)
#         print(serialized_book.data)
#         return Response(serialized_book.data)


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

class BookLike(APIView):
        def post(self, request, book_id):
            book = get_object_or_404(Book, id=book_id)
            if request.user in book.likes.all():
                book.likes.remove(request.user)
                return Response("좋아요", status=status.HTTP_200_OK)
            else:
                book.likes.add(request.user)
                return Response("좋아요 취소", status=status.HTTP_200_OK)