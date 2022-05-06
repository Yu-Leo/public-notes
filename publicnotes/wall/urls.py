from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('note/<int:pk>/', ViewNote.as_view(), name='note'),
    path('random_note/', random_note, name='random_note'),
    path('category/<int:pk>', ViewCategory.as_view(), name='category'),
    path('add_note/', add_note, name='add_note'),
    path('authors/', ViewAuthors.as_view(), name='authors'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
