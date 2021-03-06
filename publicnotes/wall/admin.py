from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _
from mptt.admin import MPTTModelAdmin

from wall import models


class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'rating', 'stared', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'category')

    fields = ('title', 'is_public', 'views', 'created_at', 'updated_at', 'rating', 'stared', 'category', 'tags',
              'content')
    readonly_fields = ('created_at', 'updated_at', 'rating', 'views')


class MyUserAdmin(UserAdmin):
    model = models.User

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name',
                                         'email', 'show_email', 'rating', 'photo', 'get_photo', 'bio')}),
        (_('Access rights'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('get_photo', 'rating')

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src="{obj.photo.url}" width="75">')
        else:
            return '-'

    get_photo.short_description = _('Current avatar')


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('id', 'title')


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(models.User, MyUserAdmin)
# admin.site.register(models.Note, NoteAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Tag, TagAdmin)
