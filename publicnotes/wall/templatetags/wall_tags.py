"""File with custom tags for 'wall' application"""

from django import template
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist

from wall import models
from wall import services

register = template.Library()


@register.simple_tag
def get_categories():
    """
    :return: List of all categories
    """

    return cache.get_or_set('categories', services.get_categories(), 300)


@register.simple_tag
def get_tags():
    """
    :return: List of all tags
    """
    return cache.get_or_set('tags', services.get_tags(), 300)


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
def one_note(note: models.Note,
             show_full: bool = False,
             in_profile: bool = False,
             user: models.User | AnonymousUser = AnonymousUser,
             ):
    """
    Show one note as card.
    :param note: note object
    :param show_full: display all note or only preview
    :param in_profile: display note in user's profile or no
    :param user: current user (from request)
    """
    context = {
        'note': note,
        'allow_edit': services.is_authenticated_user_the_author_of_note(user, note),
        'show_full': show_full,
        'was_updated': services.has_note_been_updated(note),
        'in_profile': in_profile,
        'is_liked': services.did_user_like_note(user, note),
        'is_disliked': services.did_user_dislike_note(user, note),
    }
    return context
