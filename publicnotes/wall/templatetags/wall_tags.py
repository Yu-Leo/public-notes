"""File with custom tags for 'wall' application"""

from django import template
from django.core.exceptions import ObjectDoesNotExist

from wall import models

register = template.Library()


@register.simple_tag
def get_categories():
    """
    :return: List of all categories
    """
    return models.Category.objects.all()


@register.simple_tag
def get_notes_count_for_author(author: models.User):
    """
    :return: Number of notes, which was created by author
    """
    return models.Note.objects.filter(author=author).count()


@register.simple_tag
def get_notes_count_for_category(category: models.Category):
    """
    :return: Number of notes in category
    """
    return models.Note.objects.filter(category=category).count()


@register.simple_tag
def get_prev_note_in_category(note: models.Note):
    """
    :return: Previous note by date of creation in category
    """
    try:
        return note.get_previous_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None


@register.simple_tag
def get_next_note_in_category(note: models.Note):
    """
    :return: Next note by date of creation in category
    """
    try:
        return note.get_next_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None


@register.inclusion_tag('wall/note_template.html')
def one_note(note: models.Note, allow_edit: bool = False, show_full: bool = False):
    """
    Show one note as card.
    :param note: note object
    :param allow_edit: display button for edit note or no
    :param show_full: display all note or only preview
    """
    # Note marks as updated if difference between
    # time of last update and creation time more than one second
    was_updated = (note.updated_at - note.created_at).total_seconds() >= 1
    context = {
        'note': note,
        'allow_edit': allow_edit,
        'show_full': show_full,
        'was_updated': was_updated,
    }
    return context


@register.simple_tag
def get_tags():
    """
    :return: List of all tags
    """
    return models.Tag.objects.all()
