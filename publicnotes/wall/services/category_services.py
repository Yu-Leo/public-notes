from mptt.querysets import TreeQuerySet

from wall.models import Category


def get_category_by_pk(pk: int) -> Category:
    """
    :return: category's object by its pk
    """
    return Category.objects.get(pk=pk)


def get_ancestors_of_category(category: Category) -> list[Category]:
    """
    :return: list with ancestors of category
    """
    ancestors_list = []
    while category:
        ancestors_list.append(category)
        category = category.parent
    return list(reversed(ancestors_list))[:-1]


def get_children_of_category(category: Category) -> TreeQuerySet[Category]:
    """
    :return: list with children of category
    """
    return category.get_children()


def get_categories() -> TreeQuerySet[Category]:
    return Category.objects.all()
