from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _

from wall import exceptions
from wall import forms
from wall import utils
from wall.models import User, Note


def delete_user(user: User) -> None:
    user.delete()


def register_user(form: forms.UserRegisterForm,
                  domain: str) -> None:
    """
    Register new user by form
    """
    user = _save_new_user_to_db(form)
    _send_user_activation_email(user, domain)


def activate_user_by_link(uidb64: str, token: str) -> User:
    """
    Activate user by activation link
    :param uidb64: activation link's 'uidb64' value
    :param token: activation link's 'token' value
    :return: user's object
    """
    user = _get_user_by_activation_link_uidb64(uidb64)

    if not utils.user_activation_token.check_token(user, token):
        raise exceptions.UserActivationError

    user.is_active = True
    user.save()
    return user


def _get_user_by_activation_link_uidb64(uidb64: str) -> User:
    """
    :param uidb64: user's activation link's 'uidb64' value
    :return: user's object
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        return User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExists):
        raise exceptions.UserActivationError


def _save_new_user_to_db(form: forms.UserRegisterForm) -> User:
    """
    Register inactive user by form and return its object
    """
    user = form.save()
    user.is_active = False
    user.save()
    return user


def _send_user_activation_email(user: User, domain: str) -> None:
    """
    Send message to user's email with link for activation user's profile
    """
    email_subject = _('Confirm E-mail')
    context = {
        'link': _generate_link_for_activate_user(domain, user),
    }
    email_message = render_to_string('wall/activate_user_message.html', context)
    email = EmailMessage(email_subject, email_message, to=[user.email])
    email.send()


def _generate_link_for_activate_user(domain: str, user: User) -> str:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = utils.user_activation_token.make_token(user)
    return 'http://' + domain + str(reverse_lazy('activate',
                                                 kwargs={'uidb64': uid, 'token': token}))


def is_some_user_authenticated(user: User | AnonymousUser) -> bool:
    """
    :param user: user's object from request
    :return: True if some user authenticated else False
    """
    return not isinstance(user, AnonymousUser)


def did_user_like_note(user: User | AnonymousUser, note: Note) -> bool:
    """
    :param user: current user (from request)
    :param note: note object
    """
    return user in note.likes.all()


def did_user_dislike_note(user: User | AnonymousUser, note: Note) -> bool:
    """
    :param user: current user (from request)
    :param note: note object
    """
    return user in note.dislikes.all()
