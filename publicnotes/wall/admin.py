from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Note, Author, Category
from .models import Note, Category, User


# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'rating', 'stared', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'category')


#
# class AuthorAdmin(admin.ModelAdmin):
#     list_display = ('id', 'nickname', 'email', 'rating')
#     list_display_links = ('id', 'nickname')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(User, UserAdmin)

admin.site.register(Note, NoteAdmin)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
