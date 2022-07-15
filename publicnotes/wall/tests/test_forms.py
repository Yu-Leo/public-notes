from django.test import TestCase
from django.utils.translation import ugettext as _

from wall.forms import UpdateProfile


class UpdateProfileFromTestCase(TestCase):
    """Test 'UpdateProfile' form"""

    @classmethod
    def setUpTestData(cls) -> None:
        data_1 = {
            'username': 'username',
            'email': 'email@email.com',
            'show_email': False,
            'first_name': 'first name',
            'last_name': 'last name',
            'bio': 'bio'
        }
        cls.form_1 = UpdateProfile(data=data_1)

        data_2 = {
            'username': 'username',
            'email': 'email@email.com',
            'show_email': False,
            'first_name': 'first name',
            'last_name': 'last name',
            'bio': 'bio ' * 21
        }
        cls.form_2 = UpdateProfile(data=data_2)

    def test_clean_bio(self):
        self.assertTrue(self.form_1.is_valid())
        self.assertEqual(self.form_1.clean_bio(), 'bio')

        self.assertFalse(self.form_2.is_valid())
        self.assertEqual(self.form_2.errors['bio'], [_('The "Bio" section should contain no more than 20 words')])
