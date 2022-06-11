from django.test import TestCase
from django.urls import reverse

from wall.models import Note, User


class IndexViewTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user_1 = User.objects.create(username='user_1',
                                         email=f'user_1@localhost',
                                         password='12345')
        for i in range(9):
            Note.objects.create(title=f'Note_{i + 1}', is_public=True)
        Note.objects.create(title='Note_11', author=cls.user_1)

    def test_index(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/index.html')
        self.assertEqual(len(response.context['page_obj']), 5)

        response = self.client.get(reverse('home') + '?page=2')
        self.assertEqual(len(response.context['page_obj']), 4)

    def test_view_note(self):
        # Test for existing note_pk
        response = self.client.get(reverse('note', kwargs={'pk': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/note.html')

        # Test for not existing note_pk
        response = self.client.get(reverse('note', kwargs={'pk': 100}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wall/404.html')
