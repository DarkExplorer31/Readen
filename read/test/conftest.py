"""Conftest for read"""

import pytest
from django.test import Client

from authentication.models import User
from read.models import Book, AudioBook


@pytest.fixture
def all_objects_fixture():
    user1 = User.objects.create(email="user@user.com", first_name="user", last_name="1")
    book1 = Book.objects.create(title="Book 1", user=user1, upload="")
    audio_book1 = AudioBook.objects.create(
        original_text=book1, original_audio="", user=user1
    )
    return user1, book1, audio_book1


@pytest.fixture
def only_book_fixture():
    user2 = User.objects.create(
        username="user3@user.com",
        email="user2@user.com",
        first_name="user2",
        last_name="2",
    )
    book2 = Book.objects.create(title="Book 1", user=user2, upload="")
    client2 = Client()
    client2.force_login(user2)
    return client2, book2


@pytest.fixture
def client_with_logged_in_user_fixture():
    user3 = User.objects.create_user(
        username="user3@user.com",
        email="user3@user.com",
        first_name="user3",
        last_name="3",
        password="password",
    )
    client = Client()
    client.force_login(user3)
    return client
