from rest_framework import serializers
from .models import Book, Review
from taggit.serializers import TagListSerializerField, TaggitSerializer
from taggit.models import Tag


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    book = serializers.SerializerMethodField()

    def get_author(self, obj):
        # print(obj["author_id"])
        return obj["author_id"]

    def get_book(self, obj):
        return obj["book_id"]

    class Meta:
        model = Review
        fields = "__all__"


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class BookTagSerializer(TaggitSerializer, serializers.ModelSerializer):
    # 태그 포함 시리얼라이저
    tags = TagListSerializerField()

    class Meta:
        model = Book
        fields = "__all__"


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = (
            "title",
            "content",
            "star",
        )


class BookSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    cover = serializers.SerializerMethodField()

    def get_author(self, obj):
        # print(obj["author_id"])
        return obj["author_id"]

    def get_category(self, obj):
        return obj["category_id"]

    def get_cover(self, obj):
        return obj["cover"]

    class Meta:
        model = Book
        fields = "__all__"
