from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext as _
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    """Main user's object"""

    email = models.EmailField(unique=True, verbose_name='E-mail')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name=_('Avatar'), blank=True)
    rating = models.IntegerField(verbose_name=_('Rating'), default=0)
    bio = models.TextField(verbose_name=_('Bio'), blank=True)
    show_email = models.BooleanField(verbose_name=_('PublicEmail'), default=False)

    def get_absolute_url(self):
        return reverse('author', kwargs={"pk": self.pk})


class Note(models.Model):
    """Note's object. Main entity in application"""

    title = models.CharField(max_length=150, verbose_name=_('Title'))
    content = models.TextField(verbose_name=_('Text'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('CreationTime'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('LastUpdateTime'))
    views = models.PositiveIntegerField(default=0, verbose_name=_('NumberOfViews'))
    rating = models.IntegerField(verbose_name=_('Rating'), default=0)
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

    def get_absolute_url(self):
        return reverse('note', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = _('Note')
        verbose_name_plural = _('Notes')
        ordering = ['-created_at', 'title']


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
