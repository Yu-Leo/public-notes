# Generated by Django 3.0.2 on 2022-05-07 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0006_auto_20220503_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='bio',
            field=models.TextField(blank=True, verbose_name='О себе'),
        ),
    ]
