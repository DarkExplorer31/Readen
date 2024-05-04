"""Tests for read utils application"""

from read.utils import TextToSpeechConverter


def test_convert_pdf_file():
    file_path = "read/test/media/test.pdf"
    expected_part_of_text = "Hac ita persuasione reducti intra moenia"
    converter = TextToSpeechConverter()
    text = converter.convert_pdf_file(file_path)
    assert expected_part_of_text in text
