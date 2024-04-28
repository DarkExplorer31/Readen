"""Tests for read application"""

import pytest

from django.urls import reverse
from django.test import Client


@pytest.mark.django_db
def test_read_corner_without_book(client_with_logged_in_user_fixture):
    url = reverse("read_corner")
    client = client_with_logged_in_user_fixture
    response = client.get(url)
    assert response.status_code == 200
    assert "Bonjour user3," in response.content.decode("utf-8")
    assert "Vous n'avez pas encore de livre" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_read_corner_with_book(only_book_fixture):
    client2, book2 = only_book_fixture
    url = reverse("read_corner")
    response = client2.get(url)
    assert response.status_code == 200
    assert "Bonjour user2," in response.content.decode("utf-8")
    assert "<h3>Book 1</h3>" in response.content.decode("utf-8")
