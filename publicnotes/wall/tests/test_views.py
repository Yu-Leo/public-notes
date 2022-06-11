from django.test import TestCase
from django.urls import reverse

from wall.models import Note, User


class IndexViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        for i in range(9):
            Note.objects.create(title=f'Note_{i + 1}', is_public=True)
        Note.objects.create(title='Note_11', author=cls.user_1)

    def test_get(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/index.html')
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)


class ViewNoteTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        cls.user_2 = User.objects.create(username='user_2',
                                         email='user_2@localhost',
                                         password='123')

        Note.objects.create(title='Note_1', is_public=True)
        Note.objects.create(title='Note_11', author=cls.user_1)

    def test_for_existing_note_pk(self):
        response = self.client.get(reverse('note', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/note.html')

    def test_for_not_existing_note_pk(self):
        response = self.client.get(reverse('note', kwargs={'pk': 999}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/404.html')

    def test_for_authenticated_author(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('note', kwargs={'pk': 2}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/note.html')

    def test_for_authenticated_not_author(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('note', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('login'))

    def test_for_anonymous_user(self):
        response = self.client.get(reverse('note', kwargs={'pk': 2}))
        self.assertRedirects(response, reverse('login'))


class RandomNoteViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        cls.user_2 = User.objects.create(username='user_2',
                                         email='user_2@localhost',
                                         password='123')

        Note.objects.create(title='Note_1', is_public=True)
        Note.objects.create(title='Note_2', author=cls.user_1)

    def test_when_notes_exist(self):
        response = self.client.get(reverse('random_note'))
        self.assertEqual(response.status_code, 302)

    def test_when_notes_are_missing(self):
        Note.objects.all().delete()  # Delete all notes (needs for this test)
        response = self.client.get(reverse('random_note'))
        self.assertRedirects(response, reverse('home'))


class AddNoteViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        cls.user_2 = User.objects.create(username='user_2',
                                         email='user_2@localhost',
                                         password='123')

        Note.objects.create(title='Note_1', is_public=True)
        Note.objects.create(title='Note_2', author=cls.user_1)

    def test_get(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')

    def test_post(self):
        self.client.force_login(self.user_1)
        data = {
            'title': 'New note',
            'content': 'Some content',
            'stared': True,
            'is_public': True,
            'is_pined': False,
        }
        response = self.client.post(reverse('add_note'), data=data)
        self.assertRedirects(response, reverse('note', kwargs={'pk': 3}))

    def test_get_with_correct_category_pk(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'), {'category': 1, })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')

    def test_get_with_incorrect_category_pk(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'), {'category': 100, })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')


class EditNoteViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        cls.user_2 = User.objects.create(username='user_2',
                                         email='user_2@localhost',
                                         password='123')

        Note.objects.create(title='Note_1', is_public=True, author=cls.user_1)

    def test_for_authenticated_author(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('edit_note', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/edit_note.html')

    def test_for_authenticated_not_author(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('edit_note', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))

    def test_post(self):
        self.client.force_login(self.user_1)
        data = {
            'title': 'New note title',
            'content': 'Some new content',
            'stared': True,
            'is_public': True,
            'is_pined': False,
        }
        response = self.client.post(reverse('edit_note', kwargs={'pk': 1}), data=data)
        self.assertRedirects(response, reverse('note', kwargs={'pk': 1}))
        self.assertEqual(Note.objects.get(pk=1).title, 'New note title')


class DeleteNoteViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1',
                                          email='user_1@localhost',
                                          password='12345')

        self.user_2 = User.objects.create(username='user_2',
                                          email='user_2@localhost',
                                          password='123')

        Note.objects.create(title='Note_1', is_public=True, author=self.user_1)

    def test_for_authenticated_author(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('delete_note', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('author', kwargs={'pk': self.user_1.pk}))
        with self.assertRaises(Note.DoesNotExist):
            Note.objects.get(pk=1)

    def test_for_authenticated_not_author(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('delete_note', kwargs={'pk': 1}))
        self.assertRedirects(response, reverse('login'))


class LikeAdnDislikeNoteViewTestCase(TestCase):

    def setUp(self) -> None:
        self.user_1 = User.objects.create(username='user_1',
                                          email='user_1@localhost',
                                          password='12345')

        self.user_2 = User.objects.create(username='user_2',
                                          email='user_2@localhost',
                                          password='123')

        self.note_1 = Note.objects.create(title='Note_1', is_public=True,
                                          author=self.user_1)

    def test_like(self):
        self.client.force_login(self.user_1)
        rating_before = self.note_1.rating
        self.client.get(reverse('like_note', kwargs={'pk': 1}))
        rating_after = self.note_1.rating
        self.assertEqual(rating_after - rating_before, 1)

    def test_dislike(self):
        self.client.force_login(self.user_1)
        rating_before = self.note_1.rating
        self.client.get(reverse('dislike_note', kwargs={'pk': 1}))
        rating_after = self.note_1.rating
        self.assertEqual(rating_before - rating_after, 1)
