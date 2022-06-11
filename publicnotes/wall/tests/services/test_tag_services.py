from django.test import TestCase

from wall import services
from wall.models import Tag


class TagServicesTestCase(TestCase):
    """Test functions from services/tag_services.py"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.tag_1 = Tag.objects.create(title='Tag_1')
        cls.tag_2 = Tag.objects.create(title='Tag_2')

    def test_get_tag_by_pk(self):
        tag = self.tag_1
        result = services.get_tag_by_pk(1)
        self.assertEqual(result, tag)

    def test_get_tags(self):
        result = services.get_tags()
        self.assertEqual(set(result), {self.tag_1, self.tag_2})
