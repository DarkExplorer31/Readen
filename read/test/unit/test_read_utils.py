"""Tests for read utils application"""

import pytest
import os

from django.conf import settings
from datetime import timedelta
from read.utils import TextToSpeechConverter


def test_convert_pdf_file():
    file_path = "read/test/media/test.pdf"
    expected_part_of_text = "Hac ita persuasione reducti intra moenia"
    converter = TextToSpeechConverter()
    text = converter.convert_pdf_file(file_path)
    assert expected_part_of_text in text


def test_split_into_sentences():
    text1 = "Bonjour! Comment ça va? Je suis bien."
    sentences1 = TextToSpeechConverter.split_into_sentences(text1)
    assert sentences1 == ["Bonjour!", "Comment ça va?", "Je suis bien."]

    text2 = "C'est une phrase.C'est une autre phrase!"
    sentences2 = TextToSpeechConverter.split_into_sentences(text2)
    assert sentences2 == ["C'est une phrase.", "C'est une autre phrase!"]

    text3 = "Une seule phrase"
    sentences3 = TextToSpeechConverter.split_into_sentences(text3)
    assert sentences3 == ["Une seule phrase"]

    text4 = ""
    sentences4 = TextToSpeechConverter.split_into_sentences(text4)
    assert sentences4 == []


def test_replace_abbreviations():
    converter = TextToSpeechConverter()

    text1 = "Dr. Smith & Mrs. Jones"
    expected1 = "docteur Smith et madame Jones"
    result1 = converter._replace_abbreviations(text1)
    assert result1 == expected1

    text2 = "Mr. Johnson & Mrs. Williams went to the store."
    expected2 = "monsieur Johnson et madame Williams went to the store."
    result2 = converter._replace_abbreviations(text2)
    assert result2 == expected2

    text3 = "Dr. Smith & Mrs. Jones went to see Mr. Brown."
    expected3 = "docteur Smith et madame Jones went to see monsieur Brown."
    result3 = converter._replace_abbreviations(text3)
    assert result3 == expected3

    text4 = "The team met at 9 a.m."
    expected4 = "The team met at 9 a.m."
    result4 = converter._replace_abbreviations(text4)
    assert result4 == expected4


def test_remove_special_characters():
    converter = TextToSpeechConverter()

    text = "This is @ test # with $pecial characters!"
    cleaned_text = converter._remove_special_characters(text)
    assert cleaned_text == "This is  test  with pecial characters"

    empty_text = ""
    cleaned_empty_text = converter._remove_special_characters(empty_text)
    assert cleaned_empty_text == ""

    text_without_special_characters = "This is a normal text"
    cleaned_text_without_special = converter._remove_special_characters(
        text_without_special_characters
    )
    assert cleaned_text_without_special == text_without_special_characters


def test_preprocess_text():
    converter = TextToSpeechConverter()

    text_to_preprocess = (
        "<<Bonjour>> : C'est une phrase avec des chiffres"
        + " 12345 et des caractères !"
    )
    preprocessed_text = converter._preprocess_text(text_to_preprocess)
    assert (
        preprocessed_text
        == "Bonjour , C'est une phrase avec des chiffres et des caractères "
    )

    empty_text = ""
    preprocessed_empty_text = converter._preprocess_text(empty_text)
    assert preprocessed_empty_text == ""

    text_without_preprocessing = "This is a text without any preprocessing"
    text = converter._preprocess_text(text_without_preprocessing)
    assert text == text_without_preprocessing


@pytest.mark.django_db
@pytest.mark.parametrize("file_extension", ["pdf", "txt", "doc"])
def test_convert_to_speech(file_extension, only_book_fixture):
    client, book = only_book_fixture
    book.extension = file_extension
    converter = TextToSpeechConverter()
    if book.extension != "pdf":
        with pytest.raises(ValueError):
            file = "read/test/media/test.pdf"
            audio_path = converter.convert_to_speech(book, book.user, file)
        return
    file = "read/test/media/test.pdf"
    audio_path = converter.convert_to_speech(
        book, book.user, file, path_explicit="read/test/media/test2.mp3"
    )
    assert os.path.isfile(audio_path)
    os.remove(audio_path)


@pytest.mark.parametrize(
    "audio_path", ["read/test/media/test.mp3", "fake/path/to/audio.mp3"]
)
def test_get_audio_duration_mp3(audio_path):
    converter = TextToSpeechConverter()
    converter = TextToSpeechConverter()
    duration = converter.get_audio_duration(audio_path)
    if os.path.exists(audio_path):
        assert isinstance(duration, timedelta)
    else:
        assert duration is None
