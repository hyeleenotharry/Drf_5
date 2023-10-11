from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from user.models import User
from .models import Book, Author, Category, Review


# Create your tests here.
class mainPageTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.author_data = {"name": "강미강"}
        Author.objects.create(name="강미강")
        cls.category_data = {"name": "판타지"}
        Category.objects.create(name="판타지")
        cls.book_data = {
            "title": "test title",
            "content": "test content",
            "cover": "",
            "intro": "test introduction",
            "author": "강미강",
            "category": "판타지",
        }
        Book.objects.create(
            title="test title",
            content="test content",
            cover="",
            intro="test introduction",
            author=Author.objects.get(name="강미강"),
            category=Category.objects.get(name="판타지"),
        )

    def test_books_information(self):
        url = reverse("mainpage")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)


class DetailPage(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_data = {
            "email": "dlgpgl1029@gmail.com",
            "username": "hyelee",
            "nickname": "hye",
            "password": "1029",
        }
        User.objects.create_user(
            email=cls.user_data["email"],
            username=cls.user_data["username"],
            nickname=cls.user_data["nickname"],
            birthday=None,
            profile=None,
            password=cls.user_data["password"],
        )
        cls.author_data = {"name": "강미강"}
        Author.objects.create(name="강미강")
        cls.category_data = {"name": "판타지"}
        Category.objects.create(name="판타지")
        cls.book_data = {
            "title": "test title",
            "content": "test content",
            "cover": "",
            "intro": "test introduction",
            "author": "강미강",
            "category": "판타지",
        }
        Book.objects.create(
            title="test title",
            content="test content",
            cover="",
            intro="test introduction",
            author=Author.objects.get(name="강미강"),
            category=Category.objects.get(name="판타지"),
        )
        cls.review_data = {
            "title": "test review title",
            "content": "test review content",
            "book_id": "1",
            "star": "4",
        }
        Review.objects.create(
            title=cls.review_data["title"],
            content=cls.review_data["content"],
            book=Book.objects.get(id=1),
            author=User.objects.get(id=1),
        )

    def test_detail_page(self):
        book = Book.objects.get(id=1)
        url = book.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
