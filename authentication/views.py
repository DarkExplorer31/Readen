from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.views.generic import View
from django.contrib.auth.hashers import make_password

from authentication.forms import LoginForm, SignupForm


class LoginView(View):
    template_name = "authentication/login.html"
    form_class = LoginForm

    def get(self, request):
        form = self.form_class()
        message = ""
        if request.user.is_authenticated:
            return redirect("read_corner")
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                email=form.cleaned_data["email"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("read_corner")
        message = "Vos identifiants sont invalides"
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )


class SignupView(View):
    template_name = "authentication/signup.html"
    form_class = SignupForm

    def get(self, request):
        form = self.form_class()
        message = ""
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )

    def post(self, request):
        form = self.form_class(request.POST)
        message = ""
        if form.is_valid():
            user = form.save(commit=False)
            user.password = make_password(form.cleaned_data["password1"])
            user.save()
            login(request, user)
            return redirect("read_corner")
        return render(
            request,
            self.template_name,
            context={"form": form, "message": message},
        )
