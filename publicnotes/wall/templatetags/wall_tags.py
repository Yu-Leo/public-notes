from django import template
from wall.models import Category, Note
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.annotate(cnt=Count('note')).order_by('-cnt', 'title')


@register.simple_tag
def get_notes_count_for_author(author):
    return Note.objects.filter(author=author).count()


@register.simple_tag
def get_notes_count_for_category(category):
    return Note.objects.filter(category=category).count()


@register.simple_tag
def get_prev_note_in_category(note):
    try:
        return note.get_previous_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None


@register.simple_tag
def get_next_note_in_category(note):
    try:
        return note.get_next_by_created_at(category=note.category)
    except ObjectDoesNotExist:
        return None
