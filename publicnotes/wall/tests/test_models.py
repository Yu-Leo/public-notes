from django.test import TestCase

from wall.models import Note, User


class NoteTestCase(TestCase):

    @classmethod
    def setUpTestData(self):
        user_1 = User.objects.create(username='user_1', email='user_1@localhost.ru')
        user_2 = User.objects.create(username='user_2', email='user_2@localhost.ru')
        user_3 = User.objects.create(username='user_3', email='user_3@localhost.ru')

        Note.objects.create(title='Title 1')

        note_2 = Note.objects.create(title='Title 2')
        note_2.likes.set([user_1, user_2])

        note_3 = Note.objects.create(title='Title 3')
        note_3.dislikes.set([user_1, user_2])

        note_4 = Note.objects.create(title='Title 4')
        note_4.likes.set([user_1, user_2])
        note_4.dislikes.set([user_3, ])

    def setUp(self) -> None:
        self.notes = Note.objects.order_by('pk')

    def test_get_absolute_url(self):
        for i in range(len(self.notes)):
            self.assertEqual(f'/note/{i + 1}/', self.notes[i].get_absolute_url())

    def test_rating(self):
        self.assertEqual(0, self.notes[0].rating)
        self.assertEqual(2, self.notes[1].rating)
        self.assertEqual(-2, self.notes[2].rating)
        self.assertEqual(1, self.notes[3].rating)


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(self):

        for i in range(4):
            User.objects.create(username=f'user_{i}', email=f'user_{i}@localhost')

        users = User.objects.order_by('pk')

        note_1 = Note.objects.create(title='Title 1', is_public=True, author=users[1])
        note_1.likes.set([users[0], users[1]])

        note_2 = Note.objects.create(title='Title 2', is_public=True, author=users[2])
        note_2.likes.set([users[0], ])
        note_2.dislikes.set([users[1], users[2]])

        note_3 = Note.objects.create(title='Title 3', is_public=True, author=users[3])
        note_3.likes.set([users[0], ])

        note_4 = Note.objects.create(title='Title 4', is_public=True, author=users[3])
        note_4.likes.set([users[0], ])

    def setUp(self) -> None:
        self.users = User.objects.order_by('pk')

    def test_get_absolute_url(self):
        for i in range(len(self.users)):
            self.assertEqual(f'/author/{i + 1}/', self.users[i].get_absolute_url())

    def test_rating(self):
        self.assertEqual(0, self.users[0].rating)
        self.assertEqual(2, self.users[1].rating)
        self.assertEqual(-1, self.users[2].rating)
        self.assertEqual(2, self.users[3].rating)
