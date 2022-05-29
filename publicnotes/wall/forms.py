from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError

from .models import *


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'rating', 'stared', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'rating': forms.NumberInput(attrs={"class": "form-control"}),
            'stared': forms.CheckboxInput(attrs={"class": ["form-control", "form-check-input"]}),
            'category': forms.Select(attrs={"class": "form-control"}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class UpdateNote(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'rating', 'stared', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={"class": "form-control"}),
            'rating': forms.NumberInput(attrs={"class": "form-control"}),
            'stared': forms.CheckboxInput(attrs={"class": ["form-control", "form-check-input"]}),
            'category': forms.Select(attrs={"class": "form-control"}),
            'tags': forms.CheckboxSelectMultiple(),
        }


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'show_email', 'first_name', 'last_name', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control mb-2"}),
            'email': forms.EmailInput(attrs={"class": "form-control mb-2"}),
            'show_email': forms.CheckboxInput(attrs={"class": "form-check-input mb-2"}),
            'first_name': forms.TextInput(attrs={"class": "form-control mb-2"}),
            'last_name': forms.TextInput(attrs={"class": "form-control mb-2"}),
            'bio': forms.Textarea(attrs={"class": "form-control mb-2",
                                         "placeholder": "Расскажите немного о себе. Не более 20 слов"}),
        }

    def clean_bio(self):
        bio: str = self.cleaned_data['bio']

        if len(bio.split()) > 20:
            raise ValidationError('Раздел "О себе" должен содержать не более 20 слов')

        return bio


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


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль",
                                   widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password1 = forms.CharField(label="Новый пароль",
                                    widget=forms.PasswordInput(attrs={"class": "form-control"}))
    new_password2 = forms.CharField(label="Подтверждение нового пароля",
                                    widget=forms.PasswordInput(attrs={"class": "form-control"}))

    class Meta:
        model = User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control me-2"}),
        }
