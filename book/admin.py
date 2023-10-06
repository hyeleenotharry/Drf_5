from django.contrib import admin
from .models import Author, Category, Book, Review
from django import forms


# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Review)
