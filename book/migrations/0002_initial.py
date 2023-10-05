# Generated by Django 4.2.6 on 2023-10-05 14:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("book", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="review",
            name="book",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="book.book"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="book.author"
            ),
        ),
        migrations.AddField(
            model_name="book",
            name="likes",
            field=models.ManyToManyField(
                related_name="liked_books", to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
