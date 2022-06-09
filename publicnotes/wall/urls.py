from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('note/<int:pk>/', views.view_note, name='note'),
    path('random_note/', views.random_note, name='random_note'),
    path('category/<int:pk>/', views.ViewCategory.as_view(), name='category'),
    path('add_note/', views.add_note, name='add_note'),
    path('authors/', views.ViewAuthors.as_view(), name='authors'),
    path('author/<int:pk>/', views.ViewAuthor.as_view(), name='author'),
    path('registration/', views.registration, name='registration'),
    path('activate/<str:uidb64>/<str:token>/', views.activate_user, name='activate'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('about/', views.About.as_view(), name='about'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('delete_profile/', views.delete_profile, name='delete_profile'),
    path('categories_list/', views.ViewCategoriesList.as_view(), name='categories_list'),
    path('edit_note/<int:pk>/', views.edit_note, name='edit_note'),
    path('delete_note/<int:pk>/', views.delete_note, name='delete_note'),
    path('like_note/<int:pk>/', views.like_note, name='like_note'),
    path('change_password/', views.change_password, name='change_password'),
    path('search/', views.Search.as_view(), name='search'),
    path('tag/<int:pk>/', views.ViewTag.as_view(), name='tag'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    import debug_toolbar

    urlpatterns += [path('__debug__/', include(debug_toolbar.urls))]
