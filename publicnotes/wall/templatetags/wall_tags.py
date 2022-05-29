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
def get_notes_count_for_author(author):
    """
    :return: Number of notes, which was created by author
    """
    return models.Note.objects.filter(author=author).count()


@register.simple_tag
def get_notes_count_for_category(category):
    """
    :return: Number of notes in category
    """
    return models.Note.objects.filter(category=category).count()


@register.simple_tag
def get_prev_note_in_category(note):
    """
    :return: Previous note by date of creation in category
    """
    try:
        return note.get_previous_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None


@register.simple_tag
def get_next_note_in_category(note):
    """
    :return: Next note by date of creation in category
    """
    try:
        return note.get_next_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None
