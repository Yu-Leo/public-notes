from django.db import models


# Create your models here.

class Note(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField()
    stared = models.BooleanField()
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    category = models.ForeignKey('Category', on_delete=models.PROTECT)


class Author(models.Model):
    nickname = models.CharField(max_length=150)
    email = models.EmailField()
    photo = models.ImageField()
    rating = models.IntegerField()


class Category(models.Model):
    title = models.CharField(max_length=150)
