from django.test import TestCase

from wall import services
from wall.models import Note, User, Category, Tag


class ServicesTestCase(TestCase):
    """Test functions from services.py"""

    NUMBER_OF_TAGS = 2

    @classmethod
    def setUpTestData(cls) -> None:
        user_1 = User.objects.create(username=f'user_1', email=f'user_1@localhost')

        category_1 = Category.objects.create(title='Category_1')

        tag_1 = Tag.objects.create(title='Tag_1')
        tag_2 = Tag.objects.create(title='Tag_2')

        note_1 = Note.objects.create(title='Note_1',
                                     is_public=True,
                                     category=category_1,
                                     author=user_1, )
        note_1.tags.set([tag_1, tag_2])

        note_2 = Note.objects.create(title='Note_2',
                                     is_public=True, )
        note_2.tags.set([tag_2, ])

        note_3 = Note.objects.create(title='Note_3',
                                     category=category_1,
                                     author=user_1)
        note_3.tags.set([tag_1, ])

    def test_get_all_public_notes(self):
        all_public_notes = Note.objects.filter(is_public=True)

        result = services.get_all_public_notes()

        self.assertQuerysetEqual(all_public_notes,
                                 result,
                                 transform=lambda x: x)

    def test_get_public_notes_from_category(self):
        category_1 = Category.objects.get(pk=1)
        all_public_notes_in_category_1 = Note.objects.filter(is_public=True, category=category_1)

        result = services.get_public_notes_from_category(category_pk=category_1.pk)

        self.assertQuerysetEqual(all_public_notes_in_category_1,
                                 result,
                                 transform=lambda x: x)

    def test_get_public_notes_by_tag(self):
        for i in range(self.NUMBER_OF_TAGS):
            tag = Tag.objects.get(pk=i + 1)
            all_public_notes_by_tag = Note.objects.filter(is_public=True, tags__pk=tag.pk)
            result = services.get_public_notes_by_tag(tag_pk=tag.pk)
            self.assertQuerysetEqual(all_public_notes_by_tag,
                                     result,
                                     transform=lambda x: x)

    def test_get_notes_by_author(self):
        user = User.objects.get(pk=1)

        public_users_notes = Note.objects.filter(author=user, is_public=True)
        all_users_notes = Note.objects.filter(author=user)

        result_for_public_notes = services.get_notes_by_author(user.pk, include_private=False)
        result_for_all_notes = services.get_notes_by_author(user.pk, include_private=True)

        self.assertQuerysetEqual(public_users_notes,
                                 result_for_public_notes,
                                 transform=lambda x: x)
        self.assertQuerysetEqual(all_users_notes,
                                 result_for_all_notes,
                                 transform=lambda x: x)

    def test_get_note_by_pk(self):
        note = Note.objects.get(pk=1)

        result = services.get_note_by_pk(1)

        self.assertEqual(note, result)

    def test_search_note_by_title(self):
        search_result = Note.objects.filter(title__icontains='Note')

        result = services.search_note_by_title('Note')

        self.assertQuerysetEqual(search_result,
                                 result,
                                 transform=lambda x: x)

    def test_delete_note_by_pk(self):
        note = Note.objects.create(title='$')

        notes_before_delete = set(Note.objects.all())
        services.delete_note_by_pk(note.pk)
        notes_after_delete = set(Note.objects.all())

        difference = notes_before_delete - notes_after_delete

        d = {note, }
        self.assertEqual(d, difference)

    def test_get_random_note_with_notes(self):
        result = services.get_random_note()
        self.assertIsInstance(result, Note)
