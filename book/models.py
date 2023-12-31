from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager


# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"  # 없으면 admin 페이지에 Categorys 라고 표시됨


class Book(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    cover = models.ImageField(blank=True, upload_to="media/bookCover")
    author = models.ForeignKey(Author, null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        Category, blank=True, null=True, on_delete=models.SET_NULL
    )
    intro = models.TextField()
    tags = TaggableManager()
    likes = models.ManyToManyField("user.User", related_name="liked_books", blank=True)

    def get_absolute_url(self):
        return reverse("detail-book", kwargs={"book_id": self.pk})

    def __str__(self) -> str:
        return self.title


num_choices = zip(range(0, 6), range(0, 6))


class Review(models.Model):
    title = models.CharField(max_length=250, default="")
    author = models.ForeignKey("user.User", on_delete=models.CASCADE)
    book = models.ForeignKey(
        Book, on_delete=models.CASCADE
    )  # 역참조이므로 related_at 을 써주지 않아도 review_set 이 디폴트로 있음
    content = models.TextField()
    star = models.IntegerField(blank=True, null=True, choices=num_choices)
    likes = models.ManyToManyField(
        "user.User", related_name="liked_reviews", blank=True
    )
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
