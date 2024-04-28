import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib import messages


from read.forms import BookForm, TitleChangeForm
from read.models import Book, AudioBook

# from read.utils import TextToSpeechConverter
# from read.tasks import generate_audio_book


class ReadCornerView(LoginRequiredMixin, View):
    template_name = "read_corner.html"

    def get(self, request):
        context = {}
        try:
            book = Book.objects.get(user=request.user)
            context["book"] = book
        except Book.DoesNotExist:
            pass
        try:
            audio = AudioBook.objects.get(user=request.user)
            context["audio"] = audio
        except AudioBook.DoesNotExist:
            pass
        return render(request, self.template_name, context)


class UploadBookView(LoginRequiredMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = "upload_book.html"
    success_url = reverse_lazy("read_corner")

    def form_valid(self, form):
        user_books_count = Book.objects.filter(user=self.request.user).count()
        if user_books_count >= 1:
            form.add_error(
                None,
                "Votre livre n'a pas pu être téléversé, il semble "
                + "que vous avez déjà un livre téléversé, veuillez le"
                + " supprimer avant d'en téléversé un autre.",
            )
            return self.form_invalid(form)
        book = form.save(commit=False)
        book.user = self.request.user
        book.title = str(book.title).capitalize()
        path_to_file = book.upload.path
        book.extension = os.path.splitext(path_to_file)[1][-3:].lower()
        if book.extension != "pdf":
            form.add_error(
                None,
                "Votre livre n'a pas pu être téléversé, il semble "
                + "qu'il contienne trop de caractères.",
            )
            return self.form_invalid(form)
        book.save()
        return super().form_valid(form)


class UpdateTitleView(LoginRequiredMixin, UpdateView):
    model = Book
    form_class = TitleChangeForm
    template_name = "upload_book.html"
    success_url = reverse_lazy("read_corner")

    def get_object(self, queryset=None):
        return get_object_or_404(Book, user=self.request.user)

    def form_valid(self, form):
        book = self.get_object()
        if not book:
            return redirect(reverse_lazy("read_corner"))
        book.title = form.cleaned_data["title"]
        book.save()
        return super().form_valid(form)


class DeleteBookView(LoginRequiredMixin, DeleteView):
    template_name = "delete_book.html"
    success_url = reverse_lazy("read_corner")

    def get_object(self, queryset=None):
        return get_object_or_404(Book, user=self.request.user)

    def post(self, request, *args, **kwargs):
        book = self.get_object()
        if not book:
            messages.info(request, "Vous n'avez pas de livre téléverser.")
            return redirect(reverse_lazy("read_corner"))
        book.upload.delete()
        return super().delete(request, *args, **kwargs)


def error_404(request, exception):
    return render(request, "404.html", status=404)


def error_500(request):
    return render(request, "500.html", status=500)
