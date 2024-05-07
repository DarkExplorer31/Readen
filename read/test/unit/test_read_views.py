"""Tests for read views application"""

import pytest
import os

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from read.models import Book


# Tests for read_corner only with a book
@pytest.mark.django_db
def test_read_corner_without_book(only_connected_user_fixture):
    """Test to display the read corner template without a book"""
    url = reverse("read_corner")
    client = only_connected_user_fixture
    response = client.get(url)
    assert response.status_code == 200
    assert "Bonjour user3," in response.content.decode("utf-8")
    assert "Vous n'avez pas encore de livre" in response.content.decode("utf-8")


@pytest.mark.django_db
def test_read_corner_with_book(only_book_fixture):
    """Test to display the read corner template with a book"""
    client2, book2 = only_book_fixture
    url = reverse("read_corner")
    response = client2.get(url)
    assert response.status_code == 200
    assert "Bonjour user2," in response.content.decode("utf-8")
    assert "<h3>Book 1</h3>" in response.content.decode("utf-8")


# Tests for uploading view
@pytest.mark.django_db
def test_upload_a_book_with_a_book(only_book_fixture):
    """Test to display the upload template with a book"""
    client2, book2 = only_book_fixture
    url = reverse("upload_book")
    pdf_file = open("read/test/media/test.pdf", "rb")
    pdf_content = pdf_file.read()
    pdf_file.close()
    pdf_upload = SimpleUploadedFile(
        "file.pdf", pdf_content, content_type="application/pdf"
    )
    response = client2.post(url, {"title": "New Book", "upload": pdf_upload})
    assert response.status_code == 200
    assert "il semble que vous avez déjà un livre téléversé" in response.content.decode(
        "utf-8"
    )


@pytest.mark.django_db
def test_upload_a_book(only_connected_user_fixture):
    """Test to upload a book"""
    url = reverse("upload_book")
    client = only_connected_user_fixture
    pdf_file = open("read/test/media/test.pdf", "rb")
    pdf_content = pdf_file.read()
    pdf_file.close()
    pdf_upload = SimpleUploadedFile(
        "file.pdf", pdf_content, content_type="application/pdf"
    )
    response = client.post(url, {"title": "New Book", "upload": pdf_upload})
    assert response.status_code == 302
    # Delete PDF file after test
    os.remove("media/books/file.pdf")


# Tests for update view
@pytest.mark.django_db
def test_update_without_a_book(only_connected_user_fixture):
    """Test to try the update view without a book"""
    url = reverse("update_title")
    client = only_connected_user_fixture
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_display_update_a_book(only_book_fixture):
    """Test to try the displaying of update view with a book"""
    client2, book2 = only_book_fixture
    url = reverse("update_title")
    response = client2.get(url)
    assert response.status_code == 200
    assert "<h2>Modifier un titre du livre: Book 1</h2>" in response.content.decode(
        "utf-8"
    )


@pytest.mark.django_db
def test_update_a_book(only_book_fixture):
    """Test to try the update view with a book"""
    client2, book2 = only_book_fixture
    url = reverse("update_title")
    new_title = "New title"
    response = client2.post(url, {"title": new_title})
    assert response.status_code == 302
    assert response.url == reverse("read_corner")
    updated_book = Book.objects.get(pk=book2.pk)
    assert updated_book.title == new_title


# Tests for deleting view
@pytest.mark.django_db
def test_delete_without_a_book(only_connected_user_fixture):
    """Test to try the delete view without a book"""
    url = reverse("delete_book")
    client = only_connected_user_fixture
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_display_delete_a_book(only_book_fixture):
    """Test to try the displaying of delete view with a book"""
    client2, book2 = only_book_fixture
    url = reverse("delete_book")
    response = client2.post(url)
    assert response.status_code == 302
    assert response.url == reverse("read_corner")
    with pytest.raises(Book.DoesNotExist):
        Book.objects.get(id=book2.id)
