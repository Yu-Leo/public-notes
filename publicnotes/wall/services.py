import random

from . import exceptions
from . import forms
from . import models


def get_all_notes() -> list[models.Note]:
    """
    :return: all notes from db
    """
    return models.Note.objects.all().select_related('category', 'author')


def get_notes_from_category(category_pk: int) -> list[models.Note]:
    """
    :return: notes from category by its pk
    """
    return models.Note.objects.filter(category_id=category_pk).select_related('category', 'author')


def get_notes_by_tag(tag_pk: int) -> list[models.Note]:
    """
    :return: notes, which belong to tag with tag_pk
    """
    return models.Note.objects.filter(tags__pk=tag_pk)


def get_notes_by_author(author_pk: int) -> list[models.Note]:
    """
    :return: notes, which belong to author with tag_pk
    """
    return models.Note.objects.filter(author=author_pk)


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

    notes = get_all_notes()
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


def is_authenticated_user_the_author_of_note(authenticated_user: models.User,
                                             note_pk: int) -> bool:
    """
    :return: is authenticated_user the author of note with note_pk
    """
    return authenticated_user == models.Note.objects.get(pk=note_pk).author


def delete_user(user: models.User) -> None:
    user.delete()


def get_tag_by_pk(pk: int) -> models.Tag:
    """
    :return: tag's object by its pk
    """
    return models.Tag.objects.get(pk=pk)
