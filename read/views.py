import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.db import transaction


from read.forms import BookForm, TitleChangeForm
from read.models import Book, AudioBook
from read.utils import TextToSpeechConverter
from read.tasks import generate_audio_book


class ReadCornerView(LoginRequiredMixin, View):
    template_name = "read_corner.html"

    def get(self, request):
        try:
            book = Book.objects.get(user=request.user)
        except Book.DoesNotExist:
            context = {}
        try:
            audio = AudioBook.objects.get(user=request.user)
            context = {"book": book, "audio": audio}
        except AudioBook.DoesNotExist:
            context = {}
        return render(request, self.template_name, context)


class UploadBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "upload_book.html"
    success_url = reverse_lazy("read_corner")

    @transaction.atomic
    def form_valid(self, form):
        try:
            book = form.save(commit=False)
            book.user = self.request.user
            book.title = str(book.title).capitalize()
            path_to_file = book.upload.path
            book.extension = os.path.splitext(path_to_file)[1][-3:].lower()
            if book.extension != "pdf":
                form.add_error(
                    None,
                    "Votre livre n'a pas pu être téléversé, il semble qu'il contienne trop de caractères.",
                )
                return self.form_invalid(form)
            book.save()
            converter = TextToSpeechConverter()
            audio_path = generate_audio_book.delay(book.id, self.request.user.id)
            if not audio_path:
                form.add_error(
                    None,
                    "Votre livre n'a pas pu être téléversé.",
                )
                return self.form_invalid(form)
            audio_book = AudioBook.objects.create(
                original_text=book, original_audio=audio_path, user=self.request.user
            )
            audio_duration = converter.get_audio_duration(audio_path)
            if not audio_duration:
                form.add_error(
                    None, "Votre livre n'est pas un PDF. Seuls ce format est accepté."
                )
                return self.form_invalid(form)
            audio_book.audio_time = audio_duration
            audio_book.save()
            return super().form_valid(form)
        except Exception as e:
            print(e)
            transaction.set_rollback(True)
            if hasattr(book, "upload") and book.upload:
                if os.path.isfile(book.upload.path):
                    os.remove(book.upload.path)
            form.add_error(
                None,
                "Votre livre n'a pas pu être téléversé.",
            )
            return self.form_invalid(form)


class UpdateTitleView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = TitleChangeForm
    template_name = "upload_book.html"
    success_url = reverse_lazy("read_corner")

    def get_object(self, queryset=None):
        get_object_or_404(Book, user=self.request.user)

    def form_valid(self, form):
        book = self.get_object()
        book.title = form.cleaned_data["title"]
        book.save()
        return super().form_valid(form)


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "delete_book.html"
    success_url = reverse_lazy("read_corner")

    def get_object(self, queryset=None):
        get_object_or_404(Book, user=self.request.user)

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        book.upload.delete()
        audiobook = AudioBook.objects.filter(user=request.user).first()
        if audiobook:
            audiobook.original_audio.delete()
            audiobook.delete()
        return super().delete(request, *args, **kwargs)
