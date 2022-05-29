from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class User(AbstractUser):
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Аватарка', blank=True)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    bio = models.TextField(verbose_name='О себе', blank=True)
    show_email = models.BooleanField(verbose_name='Публичный e-mail', default=False)

    def get_absolute_url(self):
        return reverse('author', kwargs={"pk": self.pk})


class Note(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(verbose_name='Текст', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    stared = models.BooleanField(verbose_name='Важная', default=False)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор',
        null=True,
        blank=True,
    )
    category = TreeForeignKey('Category', on_delete=models.SET_NULL, verbose_name='Категория', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='notes')

    def get_absolute_url(self):
        return reverse('note', kwargs={"pk": self.pk})

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at', 'title']


class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)
    preview = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Превью', blank=True)

    def get_absolute_url(self):
        return reverse('category', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['title']
