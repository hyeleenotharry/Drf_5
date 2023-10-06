from rest_framework import serializers
from .models import Book, Review


class BookSerializer(serializers.Serializer):
    class Meta:
        model = Book
        fields = ["title", "author", "cover"]
