from django.db import models


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')
    content = models.TextField(verbose_name='Текст')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    rating = models.IntegerField(verbose_name='Рейтинг')
    stared = models.BooleanField(verbose_name='Важная')
    author = models.ForeignKey('Author', on_delete=models.PROTECT, verbose_name='Автор')
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name='Категория')

    class Meta:
        verbose_name = 'Заметка'
        verbose_name_plural = 'Заметки'
        ordering = ['-created_at', 'title']


class Author(models.Model):
    nickname = models.CharField(max_length=150, verbose_name='Никнейм')
    email = models.EmailField(verbose_name='Почта')
    photo = models.ImageField(verbose_name='Аватарка')
    rating = models.IntegerField(verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['nickname']


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']
