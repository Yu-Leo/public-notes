from django.db import models


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(verbose_name='Текст', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)
    stared = models.BooleanField(verbose_name='Важная', default=False)
    author = models.ForeignKey('Author', on_delete=models.PROTECT, verbose_name='Автор', null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория', null=True, blank=True)

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at', 'title']


class Author(models.Model):
    nickname = models.CharField(max_length=150, verbose_name='Никнейм', unique=True)
    email = models.EmailField(verbose_name='Почта', unique=True)
    photo = models.ImageField(verbose_name='Аватарка', blank=True)
    rating = models.IntegerField(verbose_name='Рейтинг', default=0)

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['nickname']


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название', unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
