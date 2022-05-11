# Generated by Django 3.0.2 on 2022-05-11 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
        migrations.AddField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Аватарка'),
        ),
        migrations.AddField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
    ]
