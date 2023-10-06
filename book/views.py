from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status, permissions
from .models import Book
from .serializers import BookSerializer


# Create your views here.
class Main(APIView):
    def get(self, request):
        # 추천 책
        books = []
        for i in range(4):
            book = get_object_or_404(Book, id=i)
            books.append(book)
        serializer = BookSerializer(books)

        # 인기 리뷰

        # 키워드

    def post(self, request):
        # 책 디테일 페이지 이동

        # 키워드 검색
        pass


class BookDetail(APIView):
    def get(self, request, book_id):
        pass


class ReviewCreate(APIView):
    def post(self, request, book_id):
        pass


class ReviewUpdate(APIView):
    def put(self, request, book_id, review_id):
        pass

    def delete(self, request, book_id, review_id):
        pass
