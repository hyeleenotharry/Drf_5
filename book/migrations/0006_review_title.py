# Generated by Django 4.2.6 on 2023-10-06 07:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("book", "0005_alter_review_star"),
    ]

    operations = [
        migrations.AddField(
            model_name="review",
            name="title",
            field=models.CharField(default="", max_length=250),
        ),
    ]