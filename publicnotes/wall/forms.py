from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from wall import models


class NoteForm(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['title', 'content', 'stared', 'category', 'tags', 'is_public', 'is_pined']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'stared': forms.CheckboxInput(attrs={'class': ['form-control', 'form-check-input']}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.CheckboxSelectMultiple(),
            'is_public': forms.CheckboxInput(attrs={'class': ['form-control', 'form-check-input']}),
            'is_pined': forms.CheckboxInput(attrs={'class': ['form-control', 'form-check-input']}),
        }


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['username', 'email', 'show_email', 'first_name', 'last_name', 'bio']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-2'}),
            'show_email': forms.CheckboxInput(attrs={'class': 'form-check-input mb-2'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-2'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mb-2',
                                         'placeholder': _('TellAboutYourself')}),
        }

    def clean_bio(self) -> str:
        """
        Clear 'bio' field. It should contain no more than 20 words
        :return: clean value of raise error
        """
        bio: str = self.cleaned_data['bio']
        if len(bio.split()) > 20:
            raise ValidationError(_('NoMoreThan20Words'))
        return bio


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label=_('Nickname'),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='E-mail',
                            widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label=_('Password'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label=_('PasswordConfirmation'),
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Nickname'),
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label=_('Password'),
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('OldPassword'),
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label=_('NewPassword'),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label=_('NewPasswordConfirmation'),
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = models.User
