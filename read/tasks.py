from celery import shared_task

from read.models import Book
from .utils import TextToSpeechConverter


@shared_task
def generate_audio_book(book_id, user_id):
    converter = TextToSpeechConverter()
    book = Book.objects.get(id=book_id)
    audio_path = converter.convert_to_speech(book, user_id, book.upload.path)
    return audio_path
