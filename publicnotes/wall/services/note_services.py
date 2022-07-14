import random

from django.contrib.auth.models import AnonymousUser
from django.db.models import F
from django.db.models.query import QuerySet

from wall import exceptions
from wall.models import Note, User


def get_all_public_notes() -> QuerySet[Note]:
    """
    :return: all public notes from db
    """
    notes = Note.objects.filter(is_public=True)
    return notes.select_related('category', 'author').prefetch_related('tags', 'likes', 'dislikes')


def get_public_notes_from_category(category_pk: int) -> list[Note]:
    """
    :return: public notes from category by its pk
    """
    return get_all_public_notes().filter(category_id=category_pk)


def get_public_notes_by_tag(tag_pk: int) -> QuerySet[Note]:
    """
    :return: public notes, which belong to tag with tag_pk
    """
    return get_all_public_notes().filter(tags__pk=tag_pk)


def get_notes_by_author(author_pk: int, include_private: bool) -> QuerySet[Note]:
    """
    :param include_private: include private notes or not
    :return: notes, which belong to author with tag_pk
    """
    all_notes = Note.objects.filter(author=author_pk)
    if not include_private:
        return all_notes.filter(is_public=True)
    return all_notes.order_by('-is_pined', '-created_at')


def get_note_by_pk(pk: int) -> Note:
    """
    :return: note's object by its pk
    """
    return Note.objects.get(pk=pk)


def search_note_by_title(title: str) -> QuerySet[Note]:
    """
    :return: notes, which title contains 'title'
    """
    return Note.objects.filter(title__icontains=title)


def delete_note_by_pk(pk: int) -> None:
    get_note_by_pk(pk).delete()


def get_random_note() -> Note:
    """
    :return: random note from note's list.
    Raise exception if there are no notes in db
    """

    notes = get_all_public_notes()
    if len(notes) > 0:
        return random.choice(notes)
    raise exceptions.ThereAreNoNotes


def add_note(data_from_form: dict, author: User) -> Note:
    """
    Add new note to db.
    :return: new note's object
    """
    tags = data_from_form.get('tags')
    del data_from_form['tags']
    data_from_form['author'] = author

    note = Note.objects.create(**data_from_form)
    note.tags.set(tags)
    return note


def increase_number_of_views(note: Note) -> None:
    """
    Increase number of views for note by 1
    """
    note.views = F('views') + 1
    note.save()
    note.refresh_from_db()


def check_right_to_read_for_note(authenticated_user: User, note: Note) -> bool:
    """
    Checks whether the note can be displayed to the requesting user
    """
    public = note.is_public
    private = not public and is_authenticated_user_the_author_of_note(
        authenticated_user=authenticated_user,
        note_pk=note.pk)
    return public or private


def is_authenticated_user_the_author_of_note(authenticated_user: User | AnonymousUser,
                                             note: Note) -> bool:
    """
    :return: is authenticated_user the author of note
    """
    return authenticated_user == note.author


def user_liked_note(user: User, note_pk: int) -> None:
    """
    User set like to note (with note_pk)
    """
    note = get_note_by_pk(note_pk)

    if user in note.dislikes.all():
        note.dislikes.remove(user)

    if user in note.likes.all():
        note.likes.remove(user)
    else:
        note.likes.add(user)

    note.recalculate_rating()


def user_disliked_note(user: User, note_pk: int) -> None:
    """
    User set dislike to note (with note_pk)
    """
    note = get_note_by_pk(note_pk)

    if user in note.likes.all():
        note.likes.remove(user)

    if user in note.dislikes.all():
        note.dislikes.remove(user)
    else:
        note.dislikes.add(user)

    note.recalculate_rating()


def has_note_been_updated(note: Note) -> bool:
    """
    Note marks as updated if difference between
    time of last update and creation time more than one second
    """
    return (note.updated_at - note.created_at).total_seconds() >= 1


def get_notes_count_for_author(user: User) -> int:
    """
    :return: Number of public notes, which was created by author
    """
    return get_notes_by_author(user.pk, include_private=False).count()
