# Generated by Django 3.1.14 on 2022-06-08 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0007_auto_20220606_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество просмотров'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='E-mail'),
        ),
    ]