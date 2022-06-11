import datetime
from unittest import mock

import pytz
from django.test import TestCase

from wall.models import Category, Tag, User, Note
from wall.templatetags import wall_tags


class WallTagsTestCase(TestCase):
    """Test wall_tags """

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username=f'user_1', email=f'user_1@localhost')
        cls.user_2 = User.objects.create(username=f'user_2', email=f'user_2@localhost')

        cls.category_1 = Category.objects.create(parent=None, title='Category_1')
        cls.tag_1 = Tag.objects.create(title='Tag_1')

        mocked_creation_time = datetime.datetime(1985, 10, 26, 1, 18, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked_creation_time)):
            cls.note_1 = Note.objects.create(title='Note_1',
                                             is_public=True,
                                             author=cls.user_1, )
            cls.note_1.likes.add(cls.user_1)
            cls.note_1.dislikes.add(cls.user_2)

            cls.note_2 = Note.objects.create(title='Note_2',
                                             author=cls.user_1, )
            cls.note_3 = Note.objects.create(title='Note_3',
                                             author=cls.user_1, )

        mocked_update_time = datetime.datetime(1985, 10, 26, 1, 20, 0, 0, tzinfo=pytz.utc)
        with mock.patch('django.utils.timezone.now', mock.Mock(return_value=mocked_update_time)):
            cls.note_2.title = 'Note_2_2'
            cls.note_2.save()

    def test_get_categories(self):
        self.assertEqual(set(wall_tags.get_categories()), {self.category_1, })

    def test_get_tags(self):
        self.assertEqual(set(wall_tags.get_tags()), {self.tag_1, })

    def test_get_notes_count_for_author(self):
        self.assertEqual(wall_tags.get_notes_count_for_author(self.user_1), 1)
        self.assertEqual(wall_tags.get_notes_count_for_author(self.user_2), 0)

    def test_get_prev_note_in_category(self):
        self.assertIsNone(wall_tags.get_prev_note_in_category(self.note_1))
        self.assertEqual(wall_tags.get_prev_note_in_category(self.note_2), self.note_1)

    def test_get_next_note_in_category(self):
        self.assertEqual(wall_tags.get_next_note_in_category(self.note_2), self.note_3)
        self.assertIsNone(wall_tags.get_next_note_in_category(self.note_3))

    def test_one_note(self):
        # Test for author
        result = wall_tags.one_note(self.note_1, user=self.user_1)
        self.assertTrue(result['allow_edit'])

        # Test for not author
        result = wall_tags.one_note(self.note_1, user=self.user_2)
        self.assertFalse(result['allow_edit'])

        # Test for user in likes
        result = wall_tags.one_note(self.note_1, user=self.user_1)
        self.assertTrue(result['is_liked'])
        self.assertFalse(result['is_disliked'])

        # Test for user in dislikes
        result = wall_tags.one_note(self.note_1, user=self.user_2)
        self.assertFalse(result['is_liked'])
        self.assertTrue(result['is_disliked'])

        # Test for user not in any reactions lists
        result = wall_tags.one_note(self.note_2, user=self.user_2)
        self.assertFalse(result['is_liked'])
        self.assertFalse(result['is_disliked'])

        # Test for updated note
        result = wall_tags.one_note(self.note_2, user=self.user_2)
        self.assertTrue(result['was_updated'])

        # Test for not updated note
        result = wall_tags.one_note(self.note_1, user=self.user_2)
        self.assertFalse(result['was_updated'])
