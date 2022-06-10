from django.db.models.query import QuerySet

from wall.models import Tag


def get_tag_by_pk(pk: int) -> Tag:
    """
    :return: tag's object by its pk
    """
    return Tag.objects.get(pk=pk)


def get_tags() -> QuerySet[Tag]:
    return Tag.objects.all()
