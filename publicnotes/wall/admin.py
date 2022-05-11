from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Note, Author, Category
from django.utils.safestring import mark_safe

from .models import Note, Category, User
from django.contrib.auth.forms import UserChangeForm


# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'rating', 'stared', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'category')


class MyUserAdmin(UserAdmin):
    model = User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name',
                                                'email', 'rating', 'photo', 'get_photo', 'bio')}),
        ('Права доступа', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Даты', {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = 'Текущая аватарка'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(User, MyUserAdmin)

admin.site.register(Note, NoteAdmin)
admin.site.register(Category, CategoryAdmin)
