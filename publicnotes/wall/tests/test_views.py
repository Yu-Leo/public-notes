from django.test import TestCase
from django.urls import reverse

from wall.models import Note, User, Category


class IndexViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user_1',
                                         email='user_1@localhost',
                                         password='12345')

        cls.user_2 = User.objects.create(username='user_2',
                                         email='user_2@localhost',
                                         password='123')
        for i in range(9):
            Note.objects.create(title=f'Note_{i + 1}', is_public=True)
        Note.objects.create(title='Note_11', author=cls.user_1)

        cls.category_1 = Category.objects.create(title='Category 1')

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/index.html')
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_view_note_for_existing_note_pk(self):
        response = self.client.get(reverse('note', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/note.html')

    def test_view_note_for_not_existing_note_pk(self):
        response = self.client.get(reverse('note', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/404.html')

    def test_view_note_for_authenticated_author(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('note', kwargs={'pk': 10}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/note.html')

    def test_view_note_for_authenticated_not_author(self):
        self.client.force_login(self.user_2)
        response = self.client.get(reverse('note', kwargs={'pk': 10}))
        self.assertRedirects(response, reverse('login'))

    def test_view_note_for_anonymous_user(self):
        response = self.client.get(reverse('note', kwargs={'pk': 10}))
        self.assertRedirects(response, reverse('login'))

    def test_random_note_when_notes_exist(self):
        response = self.client.get(reverse('random_note'))
        self.assertEqual(response.status_code, 302)

    def test_random_note_when_notes_are_missing(self):
        Note.objects.all().delete()  # Delete all notes (needs for this test)
        response = self.client.get(reverse('random_note'))
        self.assertRedirects(response, reverse('home'))

    def test_add_note_get(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')

    def test_add_note_post(self):
        self.client.force_login(self.user_1)
        data = {
            'title': 'New note',
            'content': 'Some content',
            'stared': True,
            'is_public': True,
            'is_pined': False,
        }
        response = self.client.post(reverse('add_note'), data=data)
        self.assertRedirects(response, reverse('note', kwargs={'pk': 11}))

    def test_add_note_get_with_correct_category_pk(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'), {'category': 1, })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')

    def test_add_note_get_with_incorrect_category_pk(self):
        self.client.force_login(self.user_1)
        response = self.client.get(reverse('add_note'), {'category': 100, })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/add_note_form.html')
