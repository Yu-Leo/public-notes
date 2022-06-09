# Generated by Django 3.1.14 on 2022-06-09 08:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wall', '0009_note_is_pined'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['title'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='note',
            options={'ordering': ['-created_at', 'title'], 'verbose_name': 'Note', 'verbose_name_plural': 'Notes'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['title'], 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.AlterField(
            model_name='category',
            name='parent',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='wall.category', verbose_name='Parent category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='preview',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Preview'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=150, unique=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='note',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Author'),
        ),
        migrations.AlterField(
            model_name='note',
            name='category',
            field=mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wall.category', verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='note',
            name='content',
            field=models.TextField(blank=True, verbose_name='Text'),
        ),
        migrations.AlterField(
            model_name='note',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Creation time'),
        ),
        migrations.AlterField(
            model_name='note',
            name='is_pined',
            field=models.BooleanField(default=False, verbose_name='Pined in profile'),
        ),
        migrations.AlterField(
            model_name='note',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Public'),
        ),
        migrations.AlterField(
            model_name='note',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='note',
            name='stared',
            field=models.BooleanField(default=False, verbose_name='Important'),
        ),
        migrations.AlterField(
            model_name='note',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='notes', to='wall.Tag', verbose_name='Tags'),
        ),
        migrations.AlterField(
            model_name='note',
            name='title',
            field=models.CharField(max_length=150, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='note',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Last update time'),
        ),
        migrations.AlterField(
            model_name='note',
            name='views',
            field=models.PositiveIntegerField(default=0, verbose_name='Number of views'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Title'),
        ),
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, verbose_name='Bio'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/', verbose_name='Avatar'),
        ),
        migrations.AlterField(
            model_name='user',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Rating'),
        ),
        migrations.AlterField(
            model_name='user',
            name='show_email',
            field=models.BooleanField(default=False, verbose_name='Public E-mail'),
        ),
    ]