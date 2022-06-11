from django.contrib.auth.models import AnonymousUser
from django.test import TestCase

from wall import services
from wall.models import User, Note


class UserServicesTestCase(TestCase):
    """Test functions from services/user_services.py"""

    @classmethod
    def setUpTestData(cls) -> None:
        cls.note_1 = Note.objects.create(title='Note_1')
        cls.note_2 = Note.objects.create(title='Note_2')

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username=f'user_1', email=f'user_1@localhost')
        self.user_2 = User.objects.create(username=f'user_2', email=f'user_2@localhost')

        self.note_1.likes.add(self.user_1)
        self.note_2.dislikes.add(self.user_2)

    def test_delete_user(self):
        users_before = set(User.objects.all())

        services.delete_user(self.user_1)

        users_after = set(User.objects.all())
        self.assertEqual(len(users_before - users_after), 1)

    # register_user

    # activate_user_by_link

    # _get_user_by_activation_link_uidb64

    # _save_new_user_to_db

    # _send_user_activation_email

    # _generate_link_for_activate_user

    def test_is_some_user_authenticated(self):
        self.assertTrue(services.is_some_user_authenticated(self.user_1))
        self.assertFalse(services.is_some_user_authenticated(AnonymousUser()))

    def test_did_user_like_note(self):
        self.assertTrue(services.did_user_like_note(self.user_1, self.note_1))
        self.assertFalse(services.did_user_like_note(self.user_2, self.note_1))
        self.assertFalse(services.did_user_like_note(self.user_1, self.note_2))

    def test_did_user_dislike_note(self):
        self.assertTrue(services.did_user_dislike_note(self.user_2, self.note_2))
        self.assertFalse(services.did_user_dislike_note(self.user_2, self.note_1))
        self.assertFalse(services.did_user_dislike_note(self.user_1, self.note_2))
