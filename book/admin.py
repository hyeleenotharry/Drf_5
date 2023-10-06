from django.contrib import admin
from .models import Author, Category, Book
from django import forms


# Register your models here.
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
