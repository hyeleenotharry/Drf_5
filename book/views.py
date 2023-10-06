from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Book


# Create your views here.
class Main(APIView):
    def get(self, request):
        books = []
        for i in range(4):
            book = Book.objects.filter(id=i)
            books.append(book)
