from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms


class LoginForm(forms.Form):
    email = forms.CharField(
        max_length=25,
        label="Votre Email",
        # widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
        label="Mot de Passe",
    )


class SignupForm(UserCreationForm):
    email = (
        forms.EmailField()
    )  # widget=forms.TextInput(attrs={"class": "form-control"}))
    first_name = forms.CharField(
        # widget=forms.TextInput(attrs={"class": "form-control"})
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))

    password1 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(),
        label="Mot de Passe",
        help_text="Votre mot de passe doit contenir au moins 8 caractères et inclure des chiffres, des lettres majuscules et minuscules.",
    )

    password2 = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(),
        label="Confirmation de mot de Passe",
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ["email", "first_name", "last_name", "password1", "password2"]
