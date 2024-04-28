from django.db import models

from authentication.models import User


class Book(models.Model):
    title = models.CharField(
        max_length=255,
        editable=True,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="book")
    upload = models.FileField(upload_to="books/")
    upload_time = models.DateTimeField(auto_now_add=True)
    extension = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.title


class AudioBook(models.Model):
    original_text = models.OneToOneField(
        Book, on_delete=models.CASCADE, related_name="audio_book"
    )
    audio_time = models.DurationField(null=True, blank=True)
    original_audio = models.FileField(upload_to="audios/")
    audio_created_time = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="audio_book_user"
    )

    def __str__(self):
        return f"{self.original_text.title} - {self.audio_created_time}"
