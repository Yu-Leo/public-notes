# Generated by Django 3.1.14 on 2022-05-27 14:42

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wall.category', verbose_name='Категория'),
        ),
    ]
