from django import forms
from read.models import Book


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title", "upload"]


class TitleChangeForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["title"]
