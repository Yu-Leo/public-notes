from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from .models import Note, Author, Category
from .models import Note, Category, User
from django.contrib.auth.forms import UserChangeForm


# Register your models here.

class NoteAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'rating', 'stared', 'category')
    list_display_links = ('id', 'title')
    list_filter = ('created_at', 'category')


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('rating',)}),
    )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


admin.site.register(User, MyUserAdmin)

admin.site.register(Note, NoteAdmin)
# admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
