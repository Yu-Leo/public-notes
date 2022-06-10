from django.test import TestCase

from wall.models import Note, User, Category, Tag


class NoteTestCase(TestCase):
    """Test 'Note' model"""

    @classmethod
    def setUpTestData(cls) -> None:
        """Create test notes objects"""
        for i in range(3):
            User.objects.create(username=f'user_{i}', email=f'user_{i}@localhost')
        users = User.objects.order_by('pk')

        Note.objects.create(title='Title 1')

        note_2 = Note.objects.create(title='Title 2')
        note_2.likes.set([users[0], users[1]])

        note_3 = Note.objects.create(title='Title 3')
        note_3.dislikes.set([users[0], users[1]])

        note_4 = Note.objects.create(title='Title 4')
        note_4.likes.set([users[0], users[1]])
        note_4.dislikes.set([users[2], ])

    def setUp(self) -> None:
        self.notes = Note.objects.order_by('pk')

    def test_get_absolute_url(self) -> None:
        for i in range(len(self.notes)):
            self.assertEqual(f'/note/{i + 1}/', self.notes[i].get_absolute_url())

    def test_rating(self) -> None:
        self.assertEqual(0, self.notes[0].rating)
        self.assertEqual(2, self.notes[1].rating)
        self.assertEqual(-2, self.notes[2].rating)
        self.assertEqual(1, self.notes[3].rating)


class UserTestCase(TestCase):
    """Test 'User' model"""

    @classmethod
    def setUpTestData(cls) -> None:
        """Create test users objects"""
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

    def test_get_absolute_url(self) -> None:
        for i in range(len(self.users)):
            self.assertEqual(f'/author/{i + 1}/', self.users[i].get_absolute_url())

    def test_rating(self) -> None:
        self.assertEqual(0, self.users[0].rating)
        self.assertEqual(2, self.users[1].rating)
        self.assertEqual(-1, self.users[2].rating)
        self.assertEqual(2, self.users[3].rating)


class CategoryTestCase(TestCase):
    """Test 'Category' model"""

    NUMBER_OF_CATEGORIES = 3

    @classmethod
    def setUpTestData(cls) -> None:
        """Create test categories objects"""
        for i in range(cls.NUMBER_OF_CATEGORIES):
            Category.objects.create(title=f'Category_{i + 1}')

    def setUp(self) -> None:
        self.categories = Category.objects.order_by('pk')

    def test_get_absolute_url(self) -> None:
        for i in range(self.NUMBER_OF_CATEGORIES):
            self.assertEqual(f'/category/{i + 1}/', self.categories[i].get_absolute_url())

    def test_object_name(self) -> None:
        for i in range(self.NUMBER_OF_CATEGORIES):
            self.assertEqual(self.categories[i].title, str(self.categories[i]))


class TagTestCase(TestCase):
    """Test 'Tag' model"""
    NUMBER_OF_TAGS = 3

    @classmethod
    def setUpTestData(cls) -> None:
        """
        Create test tags objects
        """
        for i in range(cls.NUMBER_OF_TAGS):
            Tag.objects.create(title=f'Tag_{i + 1}')

    def setUp(self) -> None:
        self.tags = Tag.objects.order_by('pk')

    def test_get_absolute_url(self) -> None:
        for i in range(self.NUMBER_OF_TAGS):
            self.assertEqual(f'/tag/{i + 1}/', self.tags[i].get_absolute_url())

    def test_object_name(self) -> None:
        for i in range(self.NUMBER_OF_TAGS):
            self.assertEqual(self.tags[i].title, str(self.tags[i]))