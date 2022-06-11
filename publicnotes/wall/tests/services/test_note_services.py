import enum
from typing import Callable
from typing import NamedTuple

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from wall import exceptions
from wall import services
from wall.models import Note, User, Category, Tag


class ReactionActions(enum.Enum):
    REMOVE = enum.auto()
    ADD = enum.auto()
    NOTHING = enum.auto()


class ReactionsDifferences(NamedTuple):
    likes_difference: set[User]
    likes_action: ReactionActions
    dislikes_difference: set[User]
    dislikes_action: ReactionActions


class NoteServicesTestCase(TestCase):
    """Test functions from services/note_services.py"""

    NUMBER_OF_TAGS = 2

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username=f'user_1', email=f'user_1@localhost')
        cls.user_2 = User.objects.create(username=f'user_2', email=f'user_2@localhost')
        cls.user_3 = User.objects.create(username=f'user_3', email=f'user_3@localhost')

        cls.category_1 = Category.objects.create(title='Category_1')

        cls.tag_1 = Tag.objects.create(title='Tag_1')
        cls.tag_2 = Tag.objects.create(title='Tag_2')

    def setUp(self) -> None:
        self.note_1 = Note.objects.create(title='Note_1',
                                          is_public=True,
                                          category=self.category_1,
                                          author=self.user_1, )

        self.note_1.tags.set([self.tag_1, self.tag_2])
        self.note_1.likes.set([self.user_2, ])
        self.note_1.dislikes.set([self.user_1, ])

        self.note_2 = Note.objects.create(title='Note_2',
                                          is_public=True, )
        self.note_2.tags.set([self.tag_2, ])

        self.note_3 = Note.objects.create(title='Note_3',
                                          category=self.category_1,
                                          author=self.user_1)
        self.note_3.tags.set([self.tag_1, ])

        self.note_4 = Note.objects.create(title='Note_4',
                                          is_public=True,
                                          author=self.user_1)

    def test_get_all_public_notes(self):
        all_public_notes = Note.objects.filter(is_public=True)

        result = services.get_all_public_notes()

        self.assertQuerysetEqual(all_public_notes,
                                 result,
                                 transform=lambda x: x)

    def test_get_public_notes_from_category(self):
        all_public_notes_in_category_1 = Note.objects.filter(is_public=True, category=self.category_1)

        result = services.get_public_notes_from_category(category_pk=self.category_1.pk)

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
        public_users_notes = Note.objects.filter(author=self.user_1, is_public=True)
        all_users_notes = Note.objects.filter(author=self.user_1)

        result_for_public_notes = services.get_notes_by_author(self.user_1.pk, include_private=False)
        result_for_all_notes = services.get_notes_by_author(self.user_1.pk, include_private=True)

        self.assertQuerysetEqual(public_users_notes,
                                 result_for_public_notes,
                                 transform=lambda x: x)
        self.assertQuerysetEqual(all_users_notes,
                                 result_for_all_notes,
                                 transform=lambda x: x)

    def test_get_note_by_pk(self):
        note = self.note_1

        result = services.get_note_by_pk(1)

        self.assertEqual(note, result)

    def test_search_note_by_title(self):
        search_result = Note.objects.filter(title__icontains='Note')

        result = services.search_note_by_title('Note')

        self.assertQuerysetEqual(search_result,
                                 result,
                                 transform=lambda x: x)

    def test_delete_note_by_pk(self):
        note = self.note_1
        notes_before_delete = set(Note.objects.all())

        services.delete_note_by_pk(note.pk)

        notes_after_delete = set(Note.objects.all())
        difference = notes_before_delete - notes_after_delete
        self.assertEqual({note, }, difference)

    def test_get_random_note_with_notes(self):
        result = services.get_random_note()
        self.assertIsInstance(result, Note)

    def test_get_random_note_without_notes(self):
        Note.objects.all().delete()  # Delete all notes (needs for this test)

        with self.assertRaises(exceptions.ThereAreNoNotes):
            services.get_random_note()

    # def test_add_note

    def test_increase_number_of_views(self):
        views_before_increase = self.note_1.views

        services.increase_number_of_views(self.note_1)

        views_after_increase = self.note_1.views
        self.assertEqual(1, views_after_increase - views_before_increase)

    def test_check_right_to_read_for_note(self):
        result_for_public_note = services.check_right_to_read_for_note(self.user_1, self.note_1)
        result_for_private_note_and_author = services.check_right_to_read_for_note(self.user_1, self.note_3)
        result_for_private_note_and_not_author = services.check_right_to_read_for_note(self.user_2, self.note_3)

        self.assertTrue(result_for_public_note)
        self.assertTrue(result_for_private_note_and_author)
        self.assertFalse(result_for_private_note_and_not_author)

    def test_is_authenticated_user_the_author_of_note(self):
        result_for_author = services.is_authenticated_user_the_author_of_note(self.user_1, self.note_1.pk)
        result_for_not_author = services.is_authenticated_user_the_author_of_note(self.user_2, self.note_1.pk)
        result_for_anonymous_user = services.is_authenticated_user_the_author_of_note(AnonymousUser(), self.note_1.pk)

        self.assertTrue(result_for_author)
        self.assertFalse(result_for_not_author)
        self.assertFalse(result_for_anonymous_user)

    def test_user_liked_note_if_user_was_in_dislikes_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_liked_note,
                                                                         self.note_1, self.user_1)

        self.assertEqual({self.user_1, }, reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.ADD, reactions_differences.likes_action)
        self.assertEqual({self.user_1, }, reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.REMOVE, reactions_differences.dislikes_action)

    def test_user_liked_note_when_user_was_in_likes_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_liked_note,
                                                                         self.note_1, self.user_2)

        self.assertEqual({self.user_2, }, reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.REMOVE, reactions_differences.likes_action)
        self.assertEqual(set(), reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.NOTHING, reactions_differences.dislikes_action)

    def test_user_liked_note_when_user_was_not_in_any_reactions_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_liked_note,
                                                                         self.note_1, self.user_3)

        self.assertEqual({self.user_3, }, reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.ADD, reactions_differences.likes_action)
        self.assertEqual(set(), reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.NOTHING, reactions_differences.dislikes_action)

    def test_user_disliked_note_if_user_was_in_dislikes_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_disliked_note,
                                                                         self.note_1, self.user_1)

        self.assertEqual(set(), reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.NOTHING, reactions_differences.likes_action)
        self.assertEqual({self.user_1, }, reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.REMOVE, reactions_differences.dislikes_action)

    def test_user_disliked_note_when_user_was_in_likes_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_disliked_note,
                                                                         self.note_1, self.user_2)

        self.assertEqual({self.user_2, }, reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.REMOVE, reactions_differences.likes_action)
        self.assertEqual({self.user_2, }, reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.ADD, reactions_differences.dislikes_action)

    def test_user_disliked_note_when_user_was_not_in_any_reactions_list(self):
        reactions_differences = self._get_likes_and_dislikes_differences(services.user_disliked_note,
                                                                         self.note_1, self.user_3)

        self.assertEqual(set(), reactions_differences.likes_difference)
        self.assertEqual(ReactionActions.NOTHING, reactions_differences.likes_action)
        self.assertEqual({self.user_3, }, reactions_differences.dislikes_difference)
        self.assertEqual(ReactionActions.ADD, reactions_differences.dislikes_action)

    @staticmethod
    def _get_likes_and_dislikes_differences(func: Callable[[User, int], None],
                                            note: Note,
                                            user: User) -> ReactionsDifferences:
        likes_before = set(note.likes.all())
        dislikes_before = set(note.dislikes.all())

        func(user, note.pk)

        likes_after = set(note.likes.all())
        dislikes_after = set(note.dislikes.all())

        likes_difference = likes_after ^ likes_before

        if user in likes_before and user not in likes_after:
            likes_action = ReactionActions.REMOVE
        elif user not in likes_before and user in likes_after:
            likes_action = ReactionActions.ADD
        else:
            likes_action = ReactionActions.NOTHING

        dislikes_difference = dislikes_after ^ dislikes_before

        if user in dislikes_before and user not in dislikes_after:
            dislikes_action = ReactionActions.REMOVE
        elif user not in dislikes_before and user in dislikes_after:
            dislikes_action = ReactionActions.ADD
        else:
            dislikes_action = ReactionActions.NOTHING

        return ReactionsDifferences(likes_difference, likes_action, dislikes_difference, dislikes_action)

    # def test_has_note_been_updated

    def test_get_notes_count_for_author(self):
        result_for_user_1 = services.get_notes_count_for_author(self.user_1)
        result_for_user_2 = services.get_notes_count_for_author(self.user_2)

        self.assertEqual(2, result_for_user_1)
        self.assertEqual(0, result_for_user_2)
