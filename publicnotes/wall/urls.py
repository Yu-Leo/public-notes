from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('note/<int:pk>/', ViewNote.as_view(), name='note'),
    path('random_note/', random_note, name='random_note'),
    path('category/<int:pk>', ViewCategory.as_view(), name='category')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
