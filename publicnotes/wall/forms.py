from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from .models import Note, Author

from .models import Note, User


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'rating', 'stared', 'category']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'rating': forms.NumberInput(attrs={"class": "form-control"}),
            'stared': forms.CheckboxInput(attrs={"class": ["form-control", "form-check-input"]}),
            'category': forms.Select(attrs={"class": "form-control"}),
        }


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'bio', 'photo']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'bio': forms.Textarea(attrs={"class": "form-control"}),
        }


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label="Никнейм",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    email = forms.CharField(label="E-mail",
                            widget=forms.EmailInput(attrs={"class": "form-control"}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))
    password2 = forms.CharField(label="Подтверждение пароля",
                                widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label="Никнейм",
                               widget=forms.TextInput(attrs={"class": "form-control"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={"class": "form-control"}))
