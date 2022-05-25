from django.conf.urls.static import static
from django.urls import path, include

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('note/<int:pk>/', ViewNote.as_view(), name='note'),
    path('random_note/', random_note, name='random_note'),
    path('category/<int:pk>/', ViewCategory.as_view(), name='category'),
    path('add_note/', add_note, name='add_note'),
    path('authors/', ViewAuthors.as_view(), name='authors'),
    path('author/<int:pk>/', ViewAuthor.as_view(), name='author'),
    path('registration/', registration, name='registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('about/', About.as_view(), name='about'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('delete_profile/', delete_profile, name='delete_profile'),
    path('categories_list/', categories_list, name='categories_list'),
    path('edit_note/<int:pk>/', edit_note, name='edit_note'),
    path('delete_note/<int:pk>/', delete_note, name='delete_note'),
    path('change_password/', change_password, name='change_password'),
    path('search/', Search.as_view(), name='search')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
