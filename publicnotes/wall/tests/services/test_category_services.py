from django.test import TestCase

from wall import services
from wall.models import Category


class NoteServicesTestCase(TestCase):
    """Test functions from services/category_services.py"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.category_1 = Category.objects.create(parent=None, title='Category_1')
        cls.category_2 = Category.objects.create(parent=cls.category_1, title='Category_2')
        cls.category_3 = Category.objects.create(parent=cls.category_1, title='Category_3')
        cls.category_4 = Category.objects.create(parent=cls.category_2, title='Category_4')

    def test_get_category_by_pk(self):
        category = self.category_1
        result = services.get_category_by_pk(1)
        self.assertEqual(category, result)

    def test_get_ancestors_of_category(self):
        result = services.get_ancestors_of_category(self.category_4)
        self.assertEqual([self.category_1, self.category_2], result)

    def test_get_children_of_category(self):
        result = services.get_children_of_category(self.category_1)
        self.assertEqual({self.category_2, self.category_3}, set(result))

    def test_get_categories(self):
        result = services.get_categories()
        self.assertEqual({self.category_1, self.category_2, self.category_3, self.category_4}, set(result))
