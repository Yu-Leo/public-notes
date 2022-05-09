from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Note, Author


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


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['nickname', 'email']
        labels = {
            'title': 'Название',
            'email': 'E-mail'
        }
        widgets = {
            'nickname': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.EmailInput(attrs={"class": "form-control"}),
        }

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if ' ' in nickname:
            raise ValidationError('Никнейм не должен содержать пробелов')
        return nickname


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
