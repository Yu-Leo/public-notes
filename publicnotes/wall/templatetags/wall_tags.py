from django import template
from wall.models import Category, Note

register = template.Library()


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_notes_count_for_author(author):
    return Note.objects.filter(author=author).count()


@register.simple_tag
def get_notes_count_for_category(category):
    return Note.objects.filter(category=category).count()
