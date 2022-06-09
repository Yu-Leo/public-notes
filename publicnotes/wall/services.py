import random

from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMessage
from django.db.models import F
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext as _

from . import exceptions
from . import forms
from . import models
from . import utils


def get_all_public_notes() -> list[models.Note]:
    """
    :return: all public notes from db
    """
    return models.Note.objects.filter(is_public=True).select_related('category', 'author')


def get_public_notes_from_category(category_pk: int) -> list[models.Note]:
    """
    :return: public notes from category by its pk
    """
    return get_all_public_notes().filter(category_id=category_pk)


def get_public_notes_by_tag(tag_pk: int) -> list[models.Note]:
    """
    :return: publicnotes, which belong to tag with tag_pk
    """
    return get_all_public_notes().filter(tags__pk=tag_pk)


def get_notes_by_author(author_pk: int, include_private: bool) -> list[models.Note]:
    """
    :param include_private: include private notes or not
    :return: notes, which belong to author with tag_pk
    """
    all_notes = models.Note.objects.filter(author=author_pk)
    if not include_private:
        return all_notes.filter(is_public=True)
    return all_notes.order_by('-is_pined', '-created_at')


def get_note_by_pk(pk: int) -> models.Note:
    """
    :return: note's object by its pk
    """
    return models.Note.objects.get(pk=pk)


def search_note_by_title(title: str) -> list[models.Note]:
    """
    :return: notes, which title contains 'title'
    """
    return models.Note.objects.filter(title__icontains=title)


def delete_note_by_pk(pk: int) -> None:
    get_note_by_pk(pk).delete()


def get_random_note() -> models.Note:
    """
    :return: random note from note's list.
    Raise exception if there are no notes in db
    """

    notes = get_all_public_notes()
    if len(notes) > 0:
        return random.choice(notes)
    raise exceptions.ThereAreNoNotes


def add_note(note_form: forms.NoteForm, author: models.User) -> models.Note:
    """
    Add new note to db.
    :return: new note's object
    """
    notes_data = note_form.cleaned_data
    tags = note_form.cleaned_data.get('tags')
    del notes_data['tags']
    notes_data['author'] = author

    note = models.Note.objects.create(**notes_data)
    note.tags.set(tags)
    return note


def increase_number_of_views(note: models.Note) -> None:
    """
    Increase number of views for note by 1
    """
    note.views = F('views') + 1
    note.save()
    note.refresh_from_db()


def check_right_to_read_for_note(authenticated_user: models.User, note: models.Note) -> bool:
    """
    Checks whether the note can be displayed to the requesting user
    """
    public = note.is_public
    private = not public and is_authenticated_user_the_author_of_note(
        authenticated_user=authenticated_user,
        note_pk=note.pk)
    return public or private


def get_category_by_pk(pk: int) -> models.Category:
    """
    :return: category's object by its pk
    """
    return models.Category.objects.get(pk=pk)


def get_ancestors_of_category(category: models.Category) -> list[models.Category]:
    """
    :return: list with ancestors of category
    """
    ancestors_list = []
    while category:
        ancestors_list.append(category)
        category = category.parent
    return list(reversed(ancestors_list))[:-1]


def get_children_of_category(category: models.Category) -> list[models.Category]:
    """
    :return: list with children of category
    """
    return category.get_children()


def get_tag_by_pk(pk: int) -> models.Tag:
    """
    :return: tag's object by its pk
    """
    return models.Tag.objects.get(pk=pk)


def is_authenticated_user_the_author_of_note(authenticated_user: models.User | AnonymousUser,
                                             note_pk: int) -> bool:
    """
    :return: is authenticated_user the author of note with note_pk
    """
    return authenticated_user == models.Note.objects.get(pk=note_pk).author


def delete_user(user: models.User) -> None:
    user.delete()


def register_user(form: forms.UserRegisterForm,
                  domain: str) -> None:
    """
    Register new user by form
    """
    user = _save_new_user_to_db(form)
    _send_user_activation_email(user, domain)


def activate_user_by_link(uidb64: str, token: str) -> models.User:
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


def _get_user_by_activation_link_uidb64(uidb64: str) -> models.User:
    """
    :param uidb64: user's activation link's 'uidb64' value
    :return: user's object
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        return models.User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, models.User.DoesNotExists):
        raise exceptions.UserActivationError


def _save_new_user_to_db(form: forms.UserRegisterForm) -> models.User:
    """
    Register inactive user by form and return its object
    """
    user = form.save()
    user.is_active = False
    user.save()
    return user


def _send_user_activation_email(user: models.User, domain: str) -> None:
    """
    Send message to user's email with link for activation user's profile
    """
    email_subject = _('ConfirmEmail')
    context = {
        'link': _generate_link_for_activate_user(domain, user),
    }
    email_message = render_to_string('wall/activate_user_message.html', context)
    email = EmailMessage(email_subject, email_message, to=[user.email])
    email.send()


def _generate_link_for_activate_user(domain: str, user: models.User) -> str:
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = utils.user_activation_token.make_token(user)
    return 'http://' + domain + str(reverse_lazy('activate',
                                                 kwargs={'uidb64': uid, 'token': token}))


def is_some_user_authenticated(user: models.User | AnonymousUser) -> bool:
    """
    :param user: user's object from request
    :return: True if some user authenticated else False
    """
    return not isinstance(user, AnonymousUser)


def did_user_like_note(user: models.User | AnonymousUser, note: models.Note) -> bool:
    """
    :param user: current user (from request)
    :param note: note object
    """
    return user in note.likes.all()


def did_user_dislike_note(user: models.User | AnonymousUser, note: models.Note) -> bool:
    """
    :param user: current user (from request)
    :param note: note object
    """
    return user in note.dislikes.all()


def user_liked_note(user: models.User, note_pk: int) -> None:
    """
    User set like to note (with note_pk)
    """
    note = get_note_by_pk(note_pk)

    if user in note.dislikes.all():
        note.dislikes.remove(user)
        increase_rating(note)

    if user in note.likes.all():
        note.likes.remove(user)
        decrease_rating(note)
    else:
        note.likes.add(user)
        increase_rating(note)


def user_disliked_note(user: models.User, note_pk: int) -> None:
    """
    User set dislike to note (with note_pk)
    """
    note = get_note_by_pk(note_pk)

    if user in note.likes.all():
        note.likes.remove(user)
        decrease_rating(note)

    if user in note.dislikes.all():
        note.dislikes.remove(user)
        increase_rating(note)
    else:
        note.dislikes.add(user)
        decrease_rating(note)


def has_note_been_updated(note: models.Note) -> bool:
    """
    Note marks as updated if difference between
    time of last update and creation time more than one second
    """
    return (note.updated_at - note.created_at).total_seconds() >= 1


def increase_rating(note: models.Note) -> None:
    """
    Increase rating of views for note by 1
    """
    note.rating = F('rating') + 1
    note.save()
    note.refresh_from_db()


def decrease_rating(note: models.Note) -> None:
    """
    Decrease rating of views for note by 1
    """
    note.rating = F('rating') - 1
    note.save()
    note.refresh_from_db()
