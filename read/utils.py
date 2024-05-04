import os
import re
from datetime import timedelta
import wave
import fitz
import pyttsx3
from django.conf import settings


class TextToSpeechConverter:
    RATE = 145

    @classmethod
    def convert_pdf_file(cls, file_path, text=""):
        first_page_to_ignore = "Table des matières"
        second_page_to_ignore = "À propos de cette édition électronique"
        first_page_to_ignore_index = 0
        second_page_to_ignore_index = 0
        pdf_document = fitz.open(file_path)
        for page_number in range(pdf_document.page_count):
            page = pdf_document[page_number]
            if first_page_to_ignore in page.get_text():
                first_page_to_ignore_index = page_number
                continue
            elif second_page_to_ignore in page.get_text():
                second_page_to_ignore_index = page_number
                continue
            if (
                first_page_to_ignore_index != 0
                and second_page_to_ignore_index != 0
                and page_number > first_page_to_ignore_index
                and page_number < second_page_to_ignore_index
            ):
                continue
            text += page.get_text()
        pdf_document.close()
        return text

    @classmethod
    def split_into_sentences(cls, text):
        delimiters = ".!? "
        sentences = []
        current_sentence = []
        for char in text:
            current_sentence.append(char)
            if char in delimiters:
                sentence = "".join(current_sentence).strip()
                if sentence:
                    sentences.append(sentence)
                current_sentence = []
        return sentences

    def _replace_abbreviations(self, text):
        abbreviations = {
            "dr.": "docteur",
            "mr.": "monsieur",
            "mrs.": "madame",
            "&": "et",
        }
        for abbreviation, full_form in abbreviations.items():
            text = text.replace(abbreviation, full_form)
        return text

    def _remove_special_characters(self, text):
        special_characters = "@#$%^*_{}[]|'\"<>/`~"
        text = "".join(char for char in text if char not in special_characters)
        return text

    def _preprocess_text(self, text):
        text = text.replace("<<", "").replace("»", "")
        text = text.replace(":", ",").replace("...", ",")
        text = text.replace(" - ", ",")
        text = text.replace("  ", " ")
        text = text.replace("-\n", "")
        text = text.replace("\n", "_ ")
        text = re.sub(r"\s[0-9]{1,5}\s", " ", text)
        text = self._replace_abbreviations(text)
        text = self._remove_special_characters(text)
        return text

    def convert_to_speech(self, book, user, file_path):
        file_type = book.extension
        if file_type == "pdf":
            text = self.convert_pdf_file(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        text = self._preprocess_text(text)
        sentences = self.split_into_sentences(text)
        engine = pyttsx3.init()
        engine.setProperty("rate", self.RATE)
        full_text = " ".join(sentences)
        audio_path = os.path.join(settings.MEDIA_ROOT, f"audios/{user.email}_audio.mp3")
        text_path = os.path.join(settings.MEDIA_ROOT, f"{user.email}_text.txt")
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(full_text)
        engine.save_to_file(full_text, audio_path)
        engine.runAndWait()
        return audio_path

    def get_audio_duration(self, audio_path):
        try:
            with wave.open(audio_path, "rb") as audio_file:
                num_frames = audio_file.getnframes()
                frame_rate = audio_file.getframerate()
                if frame_rate <= 0 or num_frames <= 0:
                    raise ValueError("Invalid frame rate or audio duration")

                duration_seconds = num_frames / float(frame_rate)
                duration_timedelta = timedelta(seconds=duration_seconds)
                return duration_timedelta
        except Exception as e:
            print(f"Error getting audio duration: {str(e)}")
            return None
