from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey


class Note(models.Model):
    """Note's object. Main entity in application"""

    title = models.CharField(max_length=150, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Text'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('CreationTime'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('LastUpdateTime'))
    views = models.PositiveIntegerField(default=0, verbose_name=_('NumberOfViews'))
    is_public = models.BooleanField(verbose_name=_('Public'), default=False)
    stared = models.BooleanField(verbose_name=_('Important'), default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Author'),
        null=True,
        blank=True,
    )
    is_pined = models.BooleanField(verbose_name=_('PinedInProfile'), default=False)
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, verbose_name=_('Category'), null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, verbose_name=_('Tags'), related_name='notes')
    likes = models.ManyToManyField('User', blank=True, verbose_name=_('NoteLikes'), related_name='liked_notes')
    dislikes = models.ManyToManyField('User', blank=True, verbose_name=_('NoteDislikes'), related_name='disliked_notes')

    rating = models.IntegerField(verbose_name=_('Rating'), default=0)

    def get_absolute_url(self):
        return reverse('note', kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            self.recalculate_rating()

    def recalculate_rating(self):
        """
        Rating calculates as difference between number of likes and number of dislikes
        """
        self.rating = len(self.likes.all()) - len(self.dislikes.all())
        self.save()
        self.author.recalculate_rating()

    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        ordering = ['-created_at', 'title']


class User(AbstractUser):
    """Main user's object"""

    email = models.EmailField(unique=True, verbose_name='E-mail')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name=_('Avatar'), blank=True)
    bio = models.TextField(verbose_name=_('Bio'), blank=True)
    show_email = models.BooleanField(verbose_name=_('PublicEmail'), default=False)
    rating = models.IntegerField(verbose_name=_('Rating'), default=0)

    def get_absolute_url(self):
        return reverse('author', kwargs={"pk": self.pk})

    def save(self, *args, **kwargs):
        creating = not self.pk
        super().save(*args, **kwargs)
        if creating:
            self.recalculate_rating()

    def recalculate_rating(self):
        """
        Rating calculates as sum of ratings of user's public notes
        """
        user_notes = Note.objects.filter(author=self, is_public=True)
        self.rating = sum(map(lambda note: note.rating, user_notes))
        self.save()


class Category(MPTTModel):
    """Category for note. Сan be nested"""

    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',
                            verbose_name=_('ParentCategory'))
    title = models.CharField(max_length=150, verbose_name=_('Title'), unique=True)
    preview = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name=_('Preview'), blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['title']


class Tag(models.Model):
    """Tag for note. One note can have multiple tags"""

    title = models.CharField(max_length=50, verbose_name=_('Title'), unique=True)

    def get_absolute_url(self):
        return reverse('tag', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['title']
