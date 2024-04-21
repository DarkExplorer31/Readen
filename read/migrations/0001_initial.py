# Generated by Django 4.2.7 on 2024-01-05 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("upload", models.FileField(upload_to="books/")),
                ("upload_time", models.DateTimeField(auto_now_add=True)),
                ("extension", models.CharField(blank=True, max_length=3, null=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="book",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AudioBook",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("audio_time", models.DurationField()),
                ("original_audio", models.FileField(upload_to="audios/")),
                ("audio_created_time", models.DateTimeField(auto_now_add=True)),
                (
                    "original_text",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audio_book",
                        to="read.book",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="audio_book_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
